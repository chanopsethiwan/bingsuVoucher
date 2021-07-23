import json
from .bingsuVoucher import PynamoBingsuVoucher
from datetime import datetime
from uuid import uuid4

# import requests


def add_voucher(event, context):
    item = event['arguments']
    voucher_item = PynamoBingsuVoucher(
        voucher_id = str(uuid4()),
        voucher_type = item['voucher_type'],
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        status = item['status'],
        title = item['title'],
        description = item.get('description', None),
        icon_name = item.get('icon_name', None)
    )
    voucher_item.save()
    return {'status': 200}

def get_voucher_by_id(event,context):
    item = event['arguments']
    voucher_id = item['voucher_id']
    iterator = PynamoBingsuVoucher.query(voucher_id)
    voucher_list = list(iterator)
    lst = []
    if len(voucher_list) > 0:
        for voucher in voucher_list:
            lst.append(voucher.returnJson())
    else:
        return {'status': 400}
    return {'status': 200,
            'data': lst}

def get_available_vouchers(event, context):
    iterator = PynamoBingsuVoucher.status_index.query("Available")
    voucher_list = list(iterator)
    lst = []
    if len(voucher_list) > 0:
        for voucher in voucher_list:
            lst.append(voucher.returnJson())
    else:
        return {'status': 400}
    return {'status': 200,
            'data': lst}