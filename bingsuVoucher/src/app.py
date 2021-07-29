import json
from .bingsuVoucher import PynamoBingsuVoucher
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid4

# import requests

# input: voucher_type, title 
def add_voucher(event, context):
    item = event['arguments']
    voucher_item = PynamoBingsuVoucher(
        voucher_id = str(uuid4()),
        voucher_type = item['voucher_type'],
        # date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        date_time = '2021-08-31',
        status = 'Available',
        title = item['title'],
        description = item.get('description', None),
        icon_name = item.get('icon_name', None),
        voucher_conditions = item.get('voucher_conditions', None),
        voucher_detail = item.get('voucher_detail', None),
        coin_needed = item.get('coin_needed', None)
    )
    voucher_item.save()
    return {'status': 200}

# input: get voucher by id
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

# input: no input
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

# todo: deduct coins from user table, get('', None)
# input: voucher_type, user_id
# author: paopao
def get_voucher_by_type(event, context):
    from pandas import DataFrame
    item = event['arguments']
    dynamodb = boto3.resource('dynamodb')
    
    # get user info.
    user_id = item['user_id']
    user_table = dynamodb.Table('BingsuUser')
    response_user = user_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    old_coins = response_user['Items'][0]['coins']

    # get voucher
    voucher_type = item['voucher_type']
    dynamodb = boto3.resource('dynamodb')
    voucher_table = dynamodb.Table('BingsuVoucher')
    response_voucher = voucher_table.query(
            IndexName='voucher_type',
            KeyConditionExpression=Key('voucher_type').eq(voucher_type))
    df = DataFrame(response_voucher['Items'])
    df = df[df['status'] == 'Available']
    if len(df) == 0:
        return {'status': 400, 'voucher_id': "No available voucher"}
    voucher_price = int(df['coin_needed'].iloc[0])
    # check transaction
    if old_coins < voucher_price:
        return {'status': 230, 'voucher_id': "User does not have enough coins"}
    else:
        # deduct coins from user
        new_coins = old_coins - voucher_price
        client_lambda = boto3.client('lambda')
        arguments = {
            "user_id": user_id,
            "coins": int(new_coins),
        }

        update_user_response = client_lambda.invoke(
            FunctionName = 'arn:aws:lambda:ap-southeast-1:405742985670:function:bingsuUser-UpdateUserFunction-9I54tc4Xyb2h',
            InvocationType = 'RequestResponse',
            Payload = json.dumps({'arguments': arguments})
        )
        update_user_status =  str(json.load(update_user_response['Payload'])['status'])
        if update_user_status == 400:
            return {'status': 400, 'voucher_id': "Failed to update user table no coins have been deducted"}

        # set voucher as Unavailable
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
            voucher_detail = str(df['voucher_detail'].iloc[0]),
            coin_needed = int(df['coin_needed'].iloc[0])
        )
        voucher_item.save()

        return {'status': 200, 'voucher_id': voucher_id}