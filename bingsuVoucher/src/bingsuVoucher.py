from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
import os

class StatusIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'status'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    status = UnicodeAttribute(hash_key=True)

class PynamoBingsuVoucher(Model):
    ''' database to store voucher '''
    class Meta:
        table_name = os.environ.get('BINGSU_VOUCHER_TABLE_NAME')
        region = 'ap-southeast-1'
    voucher_id = UnicodeAttribute(hash_key=True)
    voucher_type = UnicodeAttribute()
    date_time = UnicodeAttribute()
    status = UnicodeAttribute()
    
    status_index = StatusIndex()
    
    def returnJson(self):
        return vars(self).get('attribute_values')