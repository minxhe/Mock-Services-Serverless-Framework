from datetime import datetime
import logging
import json

log = logging.getLogger()
log.setLevel(logging.DEBUG)

def batch_payout(event, context):
    log.debug(event)

    sender_batch_id = event["body"]["sender_batch_header"].get("sender_batch_id")

    if sender_batch_id not in ("SUCCESS", "PENDING"):
        sender_batch_id = "PENDING"

    batch_status = sender_batch_id

    content = {
        "batch_header": {
            "sender_batch_header": {
                "sender_batch_id": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                "email_subject": "You have a payout!"
            },
            "payout_batch_id": "12345678",
            "batch_status": batch_status
        }
    }

    return json.dumps({
        "statusCode": 201,
        "data": content
    })

def batch_payout_details(event, context):
    log.debug(event)

    payout_batch_id = event["query"]["payout_batch_id"]

    if payout_batch_id not in ("ACKNOWLEDGED", "DENIED", "PENDING", "PROCESSING", "SUCCESS", "NEW", "CANCELED"):
        payout_batch_id = "CANCELED"

    batch_status = payout_batch_id

    content = {
        "batch_header": {
            "payout_batch_id": "12345678",
            "batch_status": batch_status,
            "sender_batch_id": "12345667",
            "time_created": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "time_completed": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "sender_batch_header": {
                "sender_batch_id": "2014021801",
                "email_subject": "You have a payout!"
             },
            "amount": {
                "value": "1.00",
                "currency": "USD"
            }
        }
    }

    return json.dumps({
        "statusCode": 200,
        "data": content
    })

