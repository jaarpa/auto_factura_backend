import logging
from fastapi_app.endpoints import router

logger = logging.getLogger(__name__)


@router.get("/status")
def get_status():
    """
    System healthcheck. Will return 200 if the app is running.
    """
    return {"status": "OK"}
