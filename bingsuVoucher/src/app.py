import json
from .bingsuVoucher import PynamoBingsuVoucher
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid4

# import requests


def add_voucher(event, context):
    item = event['arguments']
    voucher_item = PynamoBingsuVoucher(
        voucher_id = str(uuid4()),
        voucher_type = item['voucher_type'],
        # date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        date_time = '2021-08-31',
        status = item['status'],
        title = item['title'],
        description = item.get('description', None),
        icon_name = item.get('icon_name', None),
        voucher_conditions = item.get('voucher_conditions', None),
        voucher_details = item.get('voucher_details', None),
        coin_needed = item.get('coin_needed', None)
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

def get_voucher_by_type(event, context):
    from pandas import DataFrame
    item = event['arguments']
    voucher_type = item['voucher_type']
    dynamodb = boto3.resource('dynamodb')
    voucher_table = dynamodb.Table('BingsuVoucher')
    response_voucher = voucher_table.query(
            IndexName='voucher_type',
            KeyConditionExpression=Key('voucher_type').eq(voucher_type))
    df = DataFrame(response_voucher['Items'])
    df = df[df['status'] == 'Available']
    voucher_id = str(df['voucher_id'].iloc[0])
    voucher_item = PynamoBingsuVoucher(
        voucher_id = str(df['voucher_id'].iloc[0]),
        date_time = str(df['date_time'].iloc[0]),
        description = str(df['description'].iloc[0]),
        status = 'Unavailable',
        title = str(df['title'].iloc[0]),
        voucher_type = voucher_type,
        icon_name = str(df['icon_name'].iloc[0]),
        voucher_conditions = str(df['voucher_conditions'].iloc[0]),
        voucher_details = str(df['voucher_details'].iloc[0]),
        coin_needed = str(df['coin_needed'].iloc[0])
    )
    voucher_item.save()

    return {'status': 200, 'voucher_id': voucher_id}