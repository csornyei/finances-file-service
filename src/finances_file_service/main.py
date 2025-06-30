import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from finances_shared.params import RabbitMQParams

import finances_file_service.params as params
from finances_file_service.logger import logger
from finances_file_service.producer import producer
from finances_file_service.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        params = RabbitMQParams.from_env(logger)
        await producer.connect(params, logger)
        yield
    finally:
        if producer:
            producer.close()


app = FastAPI(lifespan=lifespan)


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


@app.middleware("http")
async def handle_exceptions(request: Request, call_next):
    """
    Middleware to handle exceptions and log them.
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exception:
        logger.error(f"HTTP exception: {http_exception.detail}")
        return {"error": http_exception.detail}, http_exception.status_code
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {"error": "Internal Server Error"}, 500


app.include_router(router, prefix="/api/v1", tags=["api"])


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    """
    params.get_file_handler()
    params.get_local_file_path()

    return {"status": "ok"}
