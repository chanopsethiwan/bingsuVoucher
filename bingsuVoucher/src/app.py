import json
from .bingsuVoucher import PynamoBingsuVoucher
from datetime import datetime

# import requests


def add_voucher(event, context):
    item = event['arguments']
    voucher_item = PynamoBingsuUser(
        voucher_id = item['voucher_id'],
        voucher_type = item['voucher_type'],
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        status = item['status']
    )
    user_item.save()
    return {'status': 200}

def get_voucher_by_id(event,context):
    return 'Hello World'