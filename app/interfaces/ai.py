from abc import ABC, abstractmethod
from typing import Dict, Any
from app.schemas import AIAnalysisResult


class BaseAIService(ABC):
    @abstractmethod
    async def evaluate_lead(
            self,
            lead_data: Dict[str, Any]
    ) -> AIAnalysisResult:
        """Analyze lead and return structured result"""
        pass
