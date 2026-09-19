from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cases import CaseCreateRequest
from app.core.orchestrator import run_investigation_pipeline
from app.core.enums import CaseState

from app.database import get_db 
from app.models.relational import Case
from app.dependencies.auth import get_current_investigator

router = APIRouter(prefix="/cases", tags=["Cases"])

@router.get("/")
def get_all_cases(
    db: Session = Depends(get_db),
    investigator: dict = Depends(get_current_investigator)
):
    cases = db.query(Case).all()
    return cases

@router.post("/new")
def create_new_case(
    request: CaseCreateRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    investigator: dict = Depends(get_current_investigator)
):
    new_case = Case(
        reported_wallet=request.reported_wallet,
        current_status=CaseState.NEW
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case) 
    
    background_tasks.add_task(
        run_investigation_pipeline, 
        case_id=new_case.id, 
        wallet=request.reported_wallet
    )
    
    return {
        "message": "Automated investigation started",
        "case_id": new_case.id,
        "victim_wallet": request.reported_wallet,
        "status": CaseState.NEW,
        "started_by": investigator["investigator_id"]
    }

@router.get("/{case_id}/status")
def get_pipeline_status(
    case_id: int, 
    db: Session = Depends(get_db),
    investigator: dict = Depends(get_current_investigator)
):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    return {
        "case_id": case_id,
        "overall_status": db_case.current_status,
        "stages": [
            {"stage": CaseState.NEW, "status": "COMPLETED"},
            {"stage": CaseState.TRACING, "status": "COMPLETED" if db_case.current_status != CaseState.NEW else "PENDING"}
        ]
    }

@router.get("/{case_id}/report")
def get_case_report(
    case_id: int, 
    db: Session = Depends(get_db),
    investigator: dict = Depends(get_current_investigator)
):
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if not db_case or db_case.current_status != CaseState.REPORT_READY:
        raise HTTPException(status_code=400, detail="Report is not ready yet")
        
    return {
        "case_id": case_id,
        "status": db_case.current_status,
        "report_metadata": {
            "title": f"Automated Investigation Report - Case {case_id}",
            "risk_assessment": "High",
        }
    }

@router.get("/{case_id}/evidence")
def get_case_evidence(
    case_id: int, 
    db: Session = Depends(get_db),
    investigator: dict = Depends(get_current_investigator)
):
    return {
        "case_id": case_id,
        "evidence_references": [
            {"type": "transaction_graph", "location": f"db_ref_{case_id}"}
        ]
    }