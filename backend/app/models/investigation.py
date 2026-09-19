import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SAEnum, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class InvestigationState(str, enum.Enum):
    NEW = "NEW"
    ANALYZING = "ANALYZING"
    TRACING = "TRACING"
    PATTERN_ANALYSIS = "PATTERN_ANALYSIS"
    RISK_ANALYSIS = "RISK_ANALYSIS"
    ATTRIBUTION = "ATTRIBUTION"
    EVIDENCE_COLLECTION = "EVIDENCE_COLLECTION"
    REPORT_GENERATION = "REPORT_GENERATION"
    REPORT_READY = "REPORT_READY"
    INVESTIGATOR_REVIEW = "INVESTIGATOR_REVIEW"
    FOLLOW_UP = "FOLLOW_UP"
    CLOSED = "CLOSED"

class StageStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class StageName(str, enum.Enum):
    INGESTION = "ingestion"
    TRACING = "tracing"
    PATTERN_DETECTION = "pattern_detection"
    RISK_ANALYSIS = "risk_analysis"
    ATTRIBUTION = "attribution"
    EVIDENCE_COLLECTION = "evidence_collection"
    REPORT_GENERATION = "report_generation"

class InvestigationRun(Base):
    __tablename__ = "investigation_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(64), unique=True, index=True, default=lambda: f"run_{uuid.uuid4().hex[:12]}")
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    current_stage = Column(SAEnum(StageName), default=StageName.INGESTION, nullable=False)
    status = Column(SAEnum(StageStatus), default=StageStatus.RUNNING, nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    failure_reason = Column(Text, nullable=True)
    run_metadata = Column(JSON, default=dict)

    case = relationship("CaseModel", back_populates="runs")
    stages = relationship("InvestigationStage", back_populates="run", cascade="all, delete-orphan")
    leads = relationship("InvestigativeLead", back_populates="run", cascade="all, delete-orphan")

class InvestigationStage(Base):
    __tablename__ = "investigation_stages"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("investigation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_name = Column(SAEnum(StageName), nullable=False)
    status = Column(SAEnum(StageStatus), default=StageStatus.PENDING, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    stage_output = Column(JSON, default=dict)
    error_message = Column(Text, nullable=True)

    run = relationship("InvestigationRun", back_populates="stages")

class InvestigativeLead(Base):
    __tablename__ = "investigative_leads"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    run_id = Column(Integer, ForeignKey("investigation_runs.id", ondelete="CASCADE"), nullable=True, index=True)
    lead_address = Column(String(128), nullable=False, index=True)
    reason_surfaced = Column(Text, nullable=False)
    supporting_tx_hashes = Column(JSON, default=list)
    detected_patterns = Column(JSON, default=list)
    confidence_score = Column(Float, nullable=False, default=0.75)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    case = relationship("CaseModel", back_populates="leads")
    run = relationship("InvestigationRun", back_populates="leads")

class ReportMetadata(Base):
    __tablename__ = "report_metadata"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(64), unique=True, index=True, default=lambda: f"rep_{uuid.uuid4().hex[:12]}")
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True)
    generation_status = Column(SAEnum(StageStatus), default=StageStatus.PENDING, nullable=False)
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    report_location = Column(String(255), nullable=True)
    report_format = Column(String(16), default="PDF")
    evidence_version = Column(String(32), default="v1.0")
    report_hash = Column(String(128), nullable=True)
    summary_data = Column(JSON, default=dict)

    case = relationship("CaseModel", back_populates="reports")