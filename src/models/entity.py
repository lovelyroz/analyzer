from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from src.core.database import Base

class Industry(Base):
    __tablename__ = "industries"

    industry_id = Column(Integer, primary_key=True, autoincrement=True)
    industry_code = Column(String(50), nullable=False, unique=True)
    industry_name = Column(String(150), nullable=False)
    parent_industry_id = Column(Integer, ForeignKey("industries.industry_id", ondelete="SET NULL"), nullable=True)

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    national_id = Column(String(20), unique=True, nullable=True)
    ticker = Column(String(50), nullable=False, unique=True)
    company_name = Column(String(200), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.industry_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)