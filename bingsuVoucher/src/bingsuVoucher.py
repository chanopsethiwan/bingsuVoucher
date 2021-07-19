from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
import os

class PynamoBingsuVoucher(Model):
    ''' database to store voucher '''
    class Meta:
        table_name = os.environ.get('BINGSU_VOUCHER_TABLE_NAME')
        region = 'ap-southeast-1'
    voucher_id = UnicodeAttribute(hash_key=True)
    voucher_type = UnicodeAttribute()
    date = UTCDateTimeAttribute()
    status = UnicodeAttribute()