from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from api.errors import AppError
from logger.logger import get_logger

logger = get_logger(__name__)

def _format_app_error(exc: AppError) -> dict:
    payload = {"detail": exc.message, "code": exc.code}
    if exc.details is not None:
        payload["details"] = exc.details
    return payload


def register_exception_handlers(app):
    @app.exception_handler(AppError)
    def app_error_handler(request: Request, exc: AppError):
        payload = _format_app_error(exc)
        # log severity by status code
        if 400 <= exc.status_code < 500:
            logger.warning("AppError: %s %s %s", request.url.path, exc.code, exc.message)
        else:
            logger.error("AppError: %s %s %s", request.url.path, exc.code, exc.message, exc_info=exc)
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    def validation_error_handler(request: Request, exc: RequestValidationError):
        # Build a concise, safe response
        details = []
        try:
            for err in exc.errors():
                details.append({"loc": err.get("loc"), "msg": err.get("msg"), "type": err.get("type")})
        except Exception:
            details = [str(exc)]
        payload = {"detail": "Validation error", "code": "validation_error", "details": details}
        logger.warning("Validation error on %s: %s", request.url.path, details)
        return JSONResponse(status_code=422, content=payload)

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        payload = {"detail": exc.detail, "code": "http_exception"}
        if hasattr(exc, "headers") and exc.headers:
            payload["details"] = dict(exc.headers)
        # 4xx are client issues
        if 400 <= exc.status_code < 500:
            logger.info("HTTPException %s %s", exc.status_code, exc.detail)
        else:
            logger.error("HTTPException %s %s", exc.status_code, exc.detail, exc_info=exc)
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception):
        # Don't leak internals; return safe message
        logger.error("Unhandled exception on %s", request.url.path, exc_info=exc)
        payload = {"detail": "Internal server error", "code": "internal_error"}
        return JSONResponse(status_code=500, content=payload)