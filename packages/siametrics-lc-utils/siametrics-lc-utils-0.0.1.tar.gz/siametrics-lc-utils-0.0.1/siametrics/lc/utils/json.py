import json
from uuid import UUID
import datetime


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)

        if isinstance(obj, (datetime.date, datetime.datetime)):
            # return str(obj)
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
