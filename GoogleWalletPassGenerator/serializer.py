from dataclasses import fields, is_dataclass
from .types import EventTicketClassId, EventTicketObjectId
from enum import Enum
import json


def serialize_to_json(data):
    def convert(o):
        if isinstance(o, Enum):
            return o.value
        if is_dataclass(o):
            dataclass_dict = {}
            for field in fields(o):
                field_value = getattr(o, field.name)
                if (field.type == EventTicketClassId or field.type == EventTicketObjectId) and field_value is not None:
                    dataclass_dict[field.name] = f'{field_value.issuerId}.{field_value.uniqueId}'
                elif field_value is not None:
                    dataclass_dict[field.name] = field_value
            return dataclass_dict
        if isinstance(o, dict):
            return {k: v for k, v in o.items() if v is not None}
        return o.__dict__

    return json.loads(json.dumps(data, default=convert))
