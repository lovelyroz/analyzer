from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint

from src.core.database import Base


class NormalizedFinancialFactInput(Base):
    """Provenance bridge for normalized facts with one or many raw inputs."""

    __tablename__ = "normalized_financial_fact_inputs"

    input_id = Column(Integer, primary_key=True, autoincrement=True)
    normalized_fact_id = Column(
        Integer,
        ForeignKey("normalized_financial_facts.fact_id"),
        nullable=False,
    )
    raw_fact_id = Column(
        Integer,
        ForeignKey("raw_financial_facts.raw_fact_id"),
        nullable=False,
    )
    mapping_decision_id = Column(
        Integer,
        ForeignKey("mapping_decisions.mapping_decision_id"),
        nullable=False,
    )
    input_role = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "input_role IN ('DIRECT','COMPONENT','TOTAL','SUBTOTAL','DISCLOSURE')",
            name="chk_normalized_input_role",
        ),
        UniqueConstraint(
            "normalized_fact_id", "raw_fact_id", "mapping_decision_id",
            name="uq_normalized_fact_input",
        ),
    )
