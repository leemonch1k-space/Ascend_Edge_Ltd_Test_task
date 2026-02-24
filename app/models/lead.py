from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.orm import relationship

from app.db import Base
from app.enums import (
    LeadSource,
    LeadStage,
    BusinessDomain,
)

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(Enum(LeadSource), nullable=False)
    stage = Column(Enum(LeadStage), default=LeadStage.NEW, nullable=False)
    business_domain = Column(Enum(BusinessDomain), nullable=True)
    activity_count = Column(Integer, default=0, nullable=False)
    ai_score = Column(Float, nullable=True)

    sale = relationship("Sale", back_populates="lead", uselist=False)
