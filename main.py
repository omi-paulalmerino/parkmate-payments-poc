import json
import os
import pytz

from bson import ObjectId
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends
from omipay import OmiPay
from pymongo.database import Database
from typing import List

from db import get_db
from models import (
  Ticket, TicketCreate, PaymentGcashCreate, PaymentGcashOrder, GcashNotifRequest
)


OMIPAY_GCASH_V1_VERSION = os.getenv("OMIPAY_GCASH_V1_VERSION")
OMIPAY_GCASH_V1_CLIENT_ID = os.getenv("OMIPAY_GCASH_V1_CLIENT_ID")


app = FastAPI()


# Dependency to get the database
def get_database(db: Database = Depends(get_db)) -> Database:
    return db


# CREATE TICKET
@app.post("/tickets", response_model=Ticket)
def ticket_create(ticket: TicketCreate, db: Database = Depends(get_database)):
    collection = db["tickets"]
    item_dict = ticket.dict()
    result = collection.insert_one(item_dict)
    return {"id": str(result.inserted_id), **item_dict}


# LIST ALL TICKET
@app.get("/tickets", response_model=List[Ticket])
def ticket_list(db: Database = Depends(get_database)):
    collection = db["tickets"]
    tickets_cursor = collection.find()
    tickets = list(tickets_cursor) # Convert cursor to list

    # Ensure each item has a proper "_id" value converted to string
    for ticket in tickets:
        ticket["id"] = str(ticket["_id"])
        del ticket["_id"]

    return tickets


# GCASH - CREATE ORDER
@app.post("/payments/gcash", response_model=PaymentGcashOrder)
def gcash_payment_create_order(input: PaymentGcashCreate):
    now_in_pht = datetime.now(pytz.timezone("Asia/Manila"))
    expiry_time = now_in_pht + timedelta(minutes=10)

    valid_order = {
      "transaction_id": input.ticket_id,
      "expiry_time": expiry_time,
      "seller": {
        "userId": "",
        "externalUserId": 1,
        "externalUserType": "externalUserType"
      },
      "buyer": {
        "userId": "",
        "externalUserId": 2,
        "externalUserType": "externalUserType"
      },
      "order_title": "Single Tenant Order",
      "order_memo": "Single Tenant Order",
      "amount": input.amount,
      "pay_return_url": "https://test.com/success",
      "cancel_return_url": "https://test.com/cancelled",
      "notification_url": "https://test.com/notify",
    }

    omipay = OmiPay()
    gcash = omipay.Gcash()
    response = gcash.create_order(**valid_order)

    return response.json()


# GCASH - NOTIFY
@app.post("/payments/gcash/notify")
def gcash_payment_notify(
  input: GcashNotifRequest,
  db: Database = Depends(get_database)
):
    omipay = OmiPay()
    gcash = omipay.Gcash()

    req_payload = input.request
    req_signature = input.signature
    func_name = req_payload.get("head").get("function")

    payload = json.dumps(req_payload, separators=(",", ":"))
    is_valid_signature = gcash.verify_signature(payload, req_signature)


    if is_valid_signature and func_name in (
      "gcash.acquiring.order.finish.notify",
      "alipayplus.acquiring.order.finish.notify",
    ):
      # ticket_id = req_payload.get("body").get("merchantTransId") # Commented for demo purposes
      ticket_id = "6786084382d0942746a557a3"
      collection = db["tickets"]

      object_id = ObjectId(ticket_id)

      # Try to update the item with the given ID
      result = collection.update_one(
          {"_id":object_id},  # Filter by item_id
          {"$set": {"is_paid": True}}  # Update the item with the new values
      )

      if result.matched_count > 0:
          print(f"********* Ticket with id='{ticket_id}' successfully PAID! *********")
      else:
          print(f"********* Ticket with id='{ticket_id}' not found *********")
      
    else:
      print("********* INVALID SIGNATURE *********") # Create Payment Event
      

    req_msg_id = req_payload.get("head").get("reqMsgId")
    response = {
      "head": {
          "version": OMIPAY_GCASH_V1_VERSION,
          "function": "gcash.acquiring.order.finish.notify",
          "clientId": OMIPAY_GCASH_V1_CLIENT_ID,
          "reqMsgId": req_msg_id,
      },
      "body": {
        "resultInfo": {
            "resultStatus": "S",
            "resultCodeId": "00000000",
            "resultCode": "SUCCESS",
            "resultMsg": "Success",
        }
      }
    }

    signature = gcash.sign(json.dumps(response))

    return {"response": response, "signature": signature.decode()}
