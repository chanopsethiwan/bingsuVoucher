import json

# import requests


def add_voucher(event, context):
    item = event['arguments']
    voucher_item = PynamoBingsuUser(
        voucher_id = item['voucher_id'],
        voucher_type = item['voucher_type'],
#         date = ,
        status = item['status']
    )
    user_item.save()
    return {'status': 200}
