from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services import LeadService
from app.ai import AIEvaluator
from app.schemas.lead import LeadCreate, LeadResponse, StageUpdate


router = APIRouter(prefix="/leads", tags=["Leads"])

def get_lead_service(db: AsyncSession = Depends(get_db)) -> LeadService:
    ai_service = AIEvaluator()
    return LeadService(db=db, ai_service=ai_service)

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_in: LeadCreate,
    service: LeadService = Depends(get_lead_service)
):
    """Create lead controller"""
    return await service.create_lead(lead_in)

@router.patch("/{lead_id}/stage", response_model=LeadResponse)
async def update_lead_stage(
    lead_id: int,
    stage_update: StageUpdate,
    service: LeadService = Depends(get_lead_service)
):
    """Update lead phase controller"""
    return await service.update_stage(lead_id, stage_update.new_stage)

@router.post("/{lead_id}/analyze")
async def analyze_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service)
):
    """AI-analyze for lead"""
    return await service.analyze_lead(lead_id)

@router.post("/{lead_id}/transfer")
async def transfer_lead_to_sales(
    lead_id: int,
    service: LeadService = Depends(get_lead_service)
):
    """Lead transfer"""
    sale = await service.transfer_to_sales(lead_id)
    return {
        "message": "Lead transferred to sales successfully",
        "sale_id": sale.id,
        "sale_stage": sale.stage.value
    }
