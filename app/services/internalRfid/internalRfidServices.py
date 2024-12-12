from sqlalchemy.orm import Session
from app.schema.vehicleRegistration import VehicleRegistration
from app.schema.allotedTags import AllotedTags
from app.models.allotedTagsBase import CreateAllotedTag,ReceiptResponse
from app.models.vehicleRegistrationBase import FetchRfidResponse,CreateVehicleRegistration,EditVehicleRegistration,DeleteVehicleRegistration,VehicleRegistrationResponse
from typing import Optional
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import random
from app.utils.webSocketManager.socketManager import WebSocketManager
import string
import asyncio
import json

# async def getRfidFromServer(websocket:WebSocket) -> FetchRfidResponse:
#     global count
#     await websocket_manager.connect(websocket)
#     try:
#         while True:            
#             # If count is odd, send "trigger" immediately
#             if count % 2 != 0:
#                 data = await websocket.receive_text()
#                 print(f"Received message: {data}, count: {count}")
#                 data_dict = json.loads(data)
#                 response = "trigger"  # Send "trigger" when count is odd
#                 # Send the response to the client
#                 await websocket_manager.send_message(response, websocket)
#                 print(f"Sent response: {response}")
            
#             # If count is even, send "stop" and just increment count without waiting for next input
#             else:
#                 response = "stop"  # Send "stop" when count is even
#                 # Send the response to the client
#                 await websocket_manager.send_message(response, websocket)
#                 print(f"Sent response: {response}")
            
#             # Increment count after sending the response
#             count += 1
#             print(f"Count after increment: {count}")

#             # **Do not wait for the next text input** when the response is "stop"
#             if response == "stop":
#                 # Simply continue with the next loop iteration
#                 print("Sent stop, waiting for next cycle where count will be odd.")
#                 continue
#     except WebSocketDisconnect:
#         await websocket_manager.disconnect(websocket)
#         print("Client disconnected")

def generate_sales_order_no():
    date_part=datetime.now().strftime("%Y-%m-%d")
    random_number = ''.join(random.choices(string.digits, k=4))
    return f"STARLABS-{date_part}-PROJECT-{random_number}"

def generate_transaction_id(vehicle_no):
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{vehicle_no}{random_string}"

def getVehicleReg(rfidTag:str,db:Session) -> Optional[VehicleRegistrationResponse]:
    vehicle=db.query(VehicleRegistration).filter_by(rfidTag=rfidTag).one_or_none()

    if vehicle is None:
        return None

    return VehicleRegistrationResponse(
        rfidTag=vehicle.rfidTag,
        typeOfVehicle=vehicle.typeOfVehicle,
        vehicleNumber=vehicle.vehicleNumber,
        doNumber=vehicle.doNumber,
        transporter=vehicle.transporter,
        driverOwner=vehicle.driverOwner,
        weighbridgeNo=vehicle.weighbridgeNo,
        visitPurpose=vehicle.visitPurpose,
        placeToVisit=vehicle.placeToVisit,
        personToVisit=vehicle.personToVisit,
        validityTill=vehicle.validityTill,
        section=vehicle.section,
        registerDate=vehicle.registerDate,
        registerTime=vehicle.registerTime
    )

def createVehicleReg(vehicleInfo:CreateVehicleRegistration,db:Session) -> bool:
    newReg=VehicleRegistration(
        rfidTag=vehicleInfo.rfidTag,
        typeOfVehicle=vehicleInfo.typeOfVehicle,
        vehicleNumber=vehicleInfo.vehicleNumber,
        doNumber=vehicleInfo.doNumber,
        transporter=vehicleInfo.transporter,
        driverOwner=vehicleInfo.driverOwner,
        weighbridgeNo=vehicleInfo.weighbridgeNo,
        visitPurpose=vehicleInfo.visitPurpose,
        placeToVisit=vehicleInfo.placeToVisit,
        personToVisit=vehicleInfo.personToVisit,
        validityTill=vehicleInfo.validityTill,
        section=vehicleInfo.section,
        registerDate=vehicleInfo.registerDate,
        registerTime=vehicleInfo.registerTime
    )

    db.add(newReg)
    db.commit()
    db.refresh(newReg)

    if(newReg):
        return True
    
    return False

def getAllotedTag(rfidTag:str,db:Session) -> Optional[ReceiptResponse]:
    tag=db.query(AllotedTags).filter_by(rfidTag=rfidTag).one_or_none()

    if tag is None:
        return None

    return ReceiptResponse(
        rfidTag=tag.rfidTag,
        typeOfVehicle=tag.typeOfVehicle,
        vehicleNumber=tag.vehicleNumber,
        salesOrder=tag.salesOrder,
        transationId=tag.transationId,
        userid=tag.userid,
        barrierGate=tag.barrierGate,
        salesType=tag.salesType,
        total=tag.total,
        regDate=tag.regDate,
        regTime=tag.regTime
    )

def createAllotedTag(dataInfo:CreateAllotedTag,db:Session) -> Optional[ReceiptResponse]:
    newTag=AllotedTags(
        rfidTag=dataInfo.rfidTag,
        typeOfVehicle=dataInfo.typeOfVehicle,
        vehicleNumber = dataInfo.vehicleNumber,
        regDate = datetime.now().strftime("%d-%m-%Y"), 
        regTime = datetime.now().strftime("%H:%M:%S HRS"),
        salesOrder = generate_sales_order_no(),
        transationId = generate_transaction_id(dataInfo.vehicleNumber),
        userid = "VAIBHAV", 
        barrierGate = "NCL BINA PROJECT MAIN BARRIER",
        salesType = "RFID ALLOCATION",
        quantity = "1", 
        total = dataInfo.total
    )

    db.add(newTag)
    db.commit()
    db.refresh(newTag)

    if(newTag):
        return ReceiptResponse(
        rfidTag=newTag.rfidTag,
        typeOfVehicle=newTag.typeOfVehicle,
        vehicleNumber=newTag.vehicleNumber,
        salesOrder=newTag.salesOrder,
        transationId=newTag.transationId,
        userid=newTag.userid,
        barrierGate=newTag.barrierGate,
        salesType=newTag.salesType,
        total=newTag.total,
        regDate=newTag.regDate,
        regTime=newTag.regTime
    )
    
    return None

def editVehicleReg(vehicleInfo:EditVehicleRegistration,db:Session) -> bool:
    vehicleReg=db.query(VehicleRegistration).filter_by(rfidTag=vehicleInfo.rfidTag).one_or_none()

    if vehicleReg is None:
        return None
    
    vehicleReg.vehicleNumber=vehicleInfo.vehicleNumber,
    vehicleReg.doNumber=vehicleInfo.doNumber,
    vehicleReg.transporter=vehicleInfo.transporter,
    vehicleReg.driverOwner=vehicleInfo.driverOwner,
    vehicleReg.weighbridgeNo=vehicleInfo.weighbridgeNo,
    vehicleReg.visitPurpose=vehicleInfo.visitPurpose,
    vehicleReg.placeToVisit=vehicleInfo.placeToVisit,
    vehicleReg.personToVisit=vehicleInfo.personToVisit,
    vehicleReg.validityTill=vehicleInfo.validityTill,
    vehicleReg.section=vehicleInfo.section

    db.commit()
    db.refresh(vehicleReg)

    return True

def deleteVehicleReg(vehicleInfo:DeleteVehicleRegistration,db:Session) -> bool:
    vehicleReg=db.query(VehicleRegistration).filter_by(rfidTag=vehicleInfo.rfidTag).one_or_none()

    if vehicleReg is None:
        return None
    
    db.delete(vehicleReg)
    db.commit()

    return True