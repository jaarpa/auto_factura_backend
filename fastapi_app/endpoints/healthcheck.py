import logging
from fastapi_app.endpoints import router
from fastapi import Depends
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

logger = logging.getLogger(__name__)


@router.get("/status")
@inject
def get_status(client_id: str = Depends(Provide["app_config.cognito.client_id"])):
    """
    System healthcheck. Will return 200 if the app is running.
    """
    return {"status": "OKisss", "client_id": client_id}
