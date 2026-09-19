from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from backend.app.models.investigation import InvestigationState, StageName, StageStatus

class StageStatusResponse(BaseModel):
    stage_name: StageName
    status: StageStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    stage_output: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class InvestigationRunResponse(BaseModel):
    run_id: str
    case_id: int
    current_stage: StageName
    status: StageStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    stages: List[StageStatusResponse] = []

class InvestigativeLeadResponse(BaseModel):
    lead_address: str
    reason_surfaced: str
    supporting_tx_hashes: List[str] = []
    detected_patterns: List[str] = []
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime

class ReportMetadataResponse(BaseModel):
    report_id: str
    case_id: int
    generation_status: StageStatus
    generated_at: datetime
    report_location: Optional[str] = None
    report_format: str
    evidence_version: str
    report_hash: Optional[str] = None

class CaseLifecycleStatusResponse(BaseModel):
    case_id: int
    reported_wallet: Optional[str] = None
    status: InvestigationState
    investigation_start_time: Optional[datetime] = None
    investigation_completion_time: Optional[datetime] = None
    report_status: str
    active_run: Optional[InvestigationRunResponse] = None
    leads_count: int = 0