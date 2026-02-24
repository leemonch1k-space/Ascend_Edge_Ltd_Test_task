from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Lead, Sale
from app.enums.customer_enums import LeadStage, SaleStage
from app.schemas import LeadCreate
from app.interfaces import BaseAIService

# Allowed transitions map
ALLOWED_TRANSITIONS = {
    LeadStage.NEW: {LeadStage.CONTACTED, LeadStage.LOST},
    LeadStage.CONTACTED: {LeadStage.QUALIFIED, LeadStage.LOST},
    LeadStage.QUALIFIED: {LeadStage.TRANSFERRED, LeadStage.LOST},
    LeadStage.TRANSFERRED: set(),
    LeadStage.LOST: set(),
}


class LeadService:
    def __init__(
            self,
            db: AsyncSession,
            ai_service: BaseAIService
    ) -> None:
        self.db = db
        self.ai_service = ai_service

    async def create_lead(self, data: LeadCreate) -> Lead:
        """Create new lead"""
        new_lead = Lead(
            source=data.source,
            business_domain=data.business_domain,
            stage=LeadStage.NEW,
            activity_count=0,
        )
        self.db.add(new_lead)
        await self.db.commit()
        await self.db.refresh(new_lead)
        return new_lead

    async def get_lead(self, lead_id: int) -> Lead:
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found"
            )
        return lead

    async def update_stage(self, lead_id: int, new_stage: LeadStage) -> Lead:
        """Update lead data && validation"""
        lead = await self.get_lead(lead_id)

        if lead.stage == LeadStage.TRANSFERRED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change stage of a transferred lead",
            )

        if new_stage not in ALLOWED_TRANSITIONS.get(lead.stage, set()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid transition from {lead.stage} to {new_stage}",
            )

        lead.stage = new_stage
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def analyze_lead(self, lead_id: int) -> dict:
        """Request to AI && result saving."""
        lead = await self.get_lead(lead_id)

        # Preparing data
        lead_data = {
            "source": lead.source.value if lead.source else None,
            "stage": lead.stage.value,
            "business_domain": (
                lead.business_domain.value if lead.business_domain else None
            ),
            "activity_count": lead.activity_count,
        }

        ai_result = await self.ai_service.evaluate_lead(lead_data)

        lead.ai_score = ai_result.score
        await self.db.commit()

        return ai_result.model_dump()

    async def transfer_to_sales(self, lead_id: int) -> Sale:
        """Transfer lead to Sales && validation."""
        lead = await self.get_lead(lead_id)

        if not lead.business_domain:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lead must have a business domain to be transferred.",
            )

        if lead.ai_score is None or lead.ai_score < 0.6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lead AI score must be evaluated and >= 0.6.",
            )

        await self.update_stage(lead.id, LeadStage.TRANSFERRED)

        new_sale = Sale(lead_id=lead.id, stage=SaleStage.NEW)
        self.db.add(new_sale)
        await self.db.commit()
        await self.db.refresh(new_sale)

        return new_sale
