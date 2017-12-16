from datetime import datetime
import boto3
import json
import os
import logging

APPBOY_NOTIFICATIONS_TABLE = os.environ["APPBOY_NOTIFICATIONS_TABLE"]
APPBOY_NOTIFICATIONS_STATUS_TABLE = os.environ["APPBOY_NOTIFICATIONS_STATUS_TABLE"]

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def notification(event, context):
    """
    event["body"]:
    {
      app_group_id: auth token
      campaign_id: one of the id below
      {
        fullyPurchased: "11111111",
        partiallyPurchased: "22222222",
        insufficientFund: "33333333"
      }
      user_id: userId //uuid user identification
    }

    expected response:
      success cases:
      1. {"message":"success"}
      2. {
            notice: 'The campaign is paused. Resume the campaign to ensure trigger requests will take effect.',
            message: 'success'
         }
    """
    log.debug(event)
    user_id = event["body"].get("user_id")
    timestamp = datetime.utcnow().isoformat() + "Z"
    campaign_id = event["body"].get("campaign_id")

    notifs = boto3.resource("dynamodb").Table(APPBOY_NOTIFICATIONS_TABLE)
    status = boto3.resource("dynamodb").Table(APPBOY_NOTIFICATIONS_STATUS_TABLE)

    if user_id and campaign_id :
        notifs.put_item(Item={
            "user_id": user_id,
            "timestamp_created": timestamp,
            "campaign_id": campaign_id
        })
    else:
        return {
            "statusCode": 404,
            "body": {
                "message": "Invalid user_id or campaign_id"
            }
        }

    notice = ""
    message = "success"

    user_status = status.query(
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id},
        ScanIndexForward = False)

    if user_status["Items"]:
        #get the lastest updated status
        user_status_lastest = user_status["Items"][0].get("status")
        if user_status_lastest == "success_paused":
            notice = "The campaign is paused. Resume the campaign to ensure trigger requests will take effect."

    response = {
        "statusCode": 200,
        "body": {
            "message": message,
            "notice": notice
        }
    }

    return response

def verification(event, context):
    log.debug(event)

    user_id = event["query"]["user_id"]

    notifs = boto3.resource("dynamodb").Table(APPBOY_NOTIFICATIONS_TABLE)

    resp = notifs.query(
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id},
        ScanIndexForward = False)

    if resp["Items"]:
        response = {
            "statusCode": 200,
            "body": {
                "notifs": resp["Items"]
            }
        }
    else:
        response = {
            "statusCode": 404,
            "body": json.dumps({"error": "No notifications found for user "+user_id })
        }

    return response

def add_status(event, context):

    status = boto3.resource("dynamodb").Table(APPBOY_NOTIFICATIONS_STATUS_TABLE)

    user_id = event["body"].get("user_id")
    timestamp = datetime.utcnow().isoformat() + "Z"
    notification_status = event["body"].get("notification_status")

    if user_id and notification_status :
        status.put_item(Item={
            "user_id": user_id,
            "timestamp_created": timestamp,
            "status": notification_status
        })
    else:
        status.put_item(Item={
            "user_id": user_id,
            "timestamp_created": timestamp,
            "status": "success"
        })

    return {
        "statusCode": 200
    }
