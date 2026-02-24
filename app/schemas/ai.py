from pydantic import BaseModel, Field

class AIAnalysisResult(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Deal probability from 0 to 1")
    recommendation: str = Field(..., description="Recommendation for sales")
    reason: str = Field(..., description="Ai decision explanation")
