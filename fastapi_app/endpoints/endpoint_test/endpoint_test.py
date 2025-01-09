import logging
from fastapi import Request
from fastapi_app.endpoints import router

logger = logging.getLogger(__name__)

@router.get("/test")
async def get_status(request: Request):
    """
    System health check. Will return 200 if the app is running.
    """
    #Inspect the contents of `request.state`
    user_data = getattr(request.state, "user", None)
    
    if user_data:
        #Using logging to print data
        logger.info(f"User data from request.state: {user_data}")
    else:
        logger.warning("No user data found in request.state")

    #You can also print directly for quick testing.
    print(f"User data: {user_data}")
    
    return {"status": "OK", "user_data": user_data}
