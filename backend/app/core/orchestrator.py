import time
import traceback
from app.core.enums import CaseState
from app.core.logging import get_logger

# Initialize the central logger for this specific file
logger = get_logger(__name__)

def update_case_status(case_id: int, new_status: CaseState):
    # Database logic temporarily bypassed until M4 finishes models
    logger.info(f"[DATABASE MOCK] Case #{case_id} status changed to: {new_status}")

def log_pipeline_failure(case_id: int, error_message: str):
    logger.error(f"[ALERT] Case #{case_id} FAILED: {error_message}")

def run_investigation_pipeline(case_id: int, wallet: str):
    logger.info(f"Starting pipeline for Case #{case_id} (Wallet: {wallet})")
    
    try:
        # 1. Tracing Stage
        update_case_status(case_id, CaseState.TRACING)
        time.sleep(1) 
        
        # 2. Pattern Analysis Stage
        update_case_status(case_id, CaseState.PATTERN_ANALYSIS)
        time.sleep(1)
        
        if wallet == "0xCRASH":
            raise ValueError("Blockchain RPC Node Timeout!")
            
        # 3. Report Generation Stage
        update_case_status(case_id, CaseState.REPORT_GENERATION)
        time.sleep(1)
        
        # 4. Finish Investigation
        update_case_status(case_id, CaseState.REPORT_READY)
        logger.info(f"Pipeline complete! Case #{case_id} is ready for investigator review.")

    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Pipeline crash trace: {error_details}")
        log_pipeline_failure(case_id, str(e))
        update_case_status(case_id, CaseState.FOLLOW_UP)