import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "127.0.0.1",
            "status_code": response.status_code,
            "duration_sec": round(process_time, 4)
        }
        
        with open("audit_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        return response
