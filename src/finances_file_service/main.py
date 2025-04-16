import time

from fastapi import FastAPI, Request

import finances_file_service.params as params
from finances_file_service.logger import logger
from finances_file_service.routes import router


app = FastAPI()


@app.middleware("http")
async def log_response(request: Request, call_next):
    """
    Middleware to log request and response details.
    """
    start_time = time.perf_counter()
    data = {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
    }
    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    data["process_time"] = process_time
    data["response"] = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
    }

    logger.info(data)

    return response


app.include_router(router, prefix="/api/v1", tags=["api"])


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    """
    params.get_file_handler()
    params.get_local_file_path()

    return {"status": "ok"}
