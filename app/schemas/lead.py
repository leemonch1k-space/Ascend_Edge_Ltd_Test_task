from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.enums.customer_enums import LeadSource, LeadStage, BusinessDomain


class LeadCreate(BaseModel):
    source: LeadSource
    business_domain: Optional[BusinessDomain] = None

class LeadResponse(BaseModel):
    id: int
    source: LeadSource
    stage: LeadStage
    business_domain: Optional[BusinessDomain]
    activity_count: int
    ai_score: Optional[float]

    model_config = ConfigDict(from_attributes=True)

class StageUpdate(BaseModel):
    new_stage: LeadStage
