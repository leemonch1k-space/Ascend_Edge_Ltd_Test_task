from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base
from app.enums import SaleStage


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    stage = Column(Enum(SaleStage), default=SaleStage.NEW, nullable=False)

    lead = relationship("Lead", back_populates="sale")
