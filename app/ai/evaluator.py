from typing import Dict, Any

from app.interfaces import BaseAIService
from app.schemas import AIAnalysisResult


class AIEvaluator(BaseAIService):
    """
    Ai-evaluator, which based on current business logic.
    Perfectly suitable as first phase before implements full-fledged ML-model
    """

    async def evaluate_lead(
            self,
            lead_data: Dict[str, Any]
    ) -> AIAnalysisResult:
        score = 0.0
        reasons = []

        # 1. Source analyze
        source = lead_data.get("source")
        if source == "partner":
            score += 0.3
            reasons.append("Partner leads have higher conversion rates.")
        elif source == "scanner":
            score += 0.1
            reasons.append("Scanner leads require more warming up.")
        elif source == "manual":
            score += 0.2
            reasons.append("Manually added leads show active interest.")

        # 2. Domain analyze
        if lead_data.get("business_domain"):
            score += 0.3
            reasons.append("Clear business domain identified.")
        else:
            reasons.append("Missing business domain lowers probability.")

        # 3. Activity analyze
        activity = lead_data.get("activity_count", 0)
        if activity > 10:
            score += 0.4
            reasons.append("High engagement rate (>10 messages).")
        elif activity > 3:
            score += 0.2
            reasons.append("Moderate engagement.")
        else:
            reasons.append("Low engagement.")

        # Constraint for AI: score can't be out of range: 0.0 - 1.0
        final_score = min(max(score, 0.0), 1.0)

        # Recommendation formatting
        if final_score >= 0.6:
            recommendation = "transfer_to_sales"
        else:
            recommendation = "nurture_lead"

        return AIAnalysisResult(
            score=round(final_score, 2),
            recommendation=recommendation,
            reason=" | ".join(reasons),
        )
