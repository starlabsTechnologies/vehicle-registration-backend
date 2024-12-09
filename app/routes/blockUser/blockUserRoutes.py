from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from app.config.db_config import get_db
from app.controllers.blockUser.blockUserController import fetchRfidTagController,getRfidDataController
from app.models.allotedTagsBase import SuccessResponse, BlockUser, ServiceResponse
from app.controllers.blockUser.blockUserController import blockUserController

blockUser_router=APIRouter()

@blockUser_router.post('/block-user',response_model=SuccessResponse)
def blockUser(userInfo:BlockUser,db:Session=Depends(get_db)):
    return blockUserController(userInfo,db)

@blockUser_router.post('/rfid-connect', response_model=ServiceResponse)
async def fetchRfidTag(request: Request):
    body = await request.json()  # Parse the raw JSON from the POST request body
    print(f"Raw JSON Body: {body}")  # Logs the incoming raw JSON payload
    
    rfid_data = await fetchRfidTagController(body)

    return ServiceResponse(
        rfid=rfid_data["rfid"],
        success=rfid_data["success"]
    )

@blockUser_router.get('/rfid-connect', response_model=ServiceResponse)
async def rfidTagRoute():
    rfid_data = await getRfidDataController()

    if rfid_data:
        return ServiceResponse(rfid=rfid_data["rfid"], success=rfid_data["success"])
    else:
        return ServiceResponse(rfid="No data", success=False)

# @blockUser_router.post('/rfid-connect', response_model=ServiceResponse)
# async def fetchRfidTag(request: Request):
#     body = await request.json()  # Parse the raw JSON from the POST request body
#     print(f"Raw JSON Body: {body}")  # Logs the incoming raw JSON payload

#     # Store the data temporarily in a global variable
#     rfid_data["rfid"] = body.get("rfid")
#     rfid_data["success"] = body.get("success")

#     # Return the same data in the response
#     return ServiceResponse(
#         rfid=rfid_data["rfid"],
#         success=rfid_data["success"]
#     )

# # The GET request handler
# @blockUser_router.get('/rfid-connect', response_model=ServiceResponse)
# async def rfidTag():
#     if not rfid_data:
#         # Trigger the POST request if no RFID data is available
#         await trigger_post_request()

#     if rfid_data:
#         return ServiceResponse(rfid=rfid_data["rfid"], success=rfid_data["success"])
#     else:
#         return ServiceResponse(rfid="No data", success=False)

# # Function to trigger a POST request to fetch RFID data
# async def trigger_post_request():
#     try:
#         # Use httpx to make the POST request
#         async with httpx.AsyncClient() as client:
#             response = await client.post("http://127.0.0.1:8000/rfid-connect", json={"rfid": "sample_rfid", "success": True})
#             if response.status_code == 200:
#                 data = response.json()
#                 rfid_data["rfid"] = data.get("rfid")
#                 rfid_data["success"] = data.get("success")
#                 print(f"Data from POST request: {rfid_data}")
#             else:
#                 print("Failed to fetch RFID data from POST request")
#     except Exception as e:
#         print(f"Error during POST request: {e}")