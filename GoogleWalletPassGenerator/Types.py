from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import List, get_args, get_origin, Iterable, Optional
from collections.abc import Iterable
from enum import Enum
import json


@dataclass
class TypeCheckedDataclass:
    def __post_init__(self):
        for f in fields(self):
            actual_value = getattr(self, f.name)
            expected_type = f.type
            origin_type = get_origin(expected_type)

            if origin_type is list or origin_type is Iterable:
                item_type = get_args(expected_type)[0]  # Get the item type
                if isinstance(actual_value, list) and not all(isinstance(item, item_type) for item in actual_value):
                    raise TypeError(
                        f'Items in field `{f.name}` are not of type `{item_type.__name__}`')
            elif not isinstance(actual_value, expected_type) and actual_value is not None:
                current_type = type(actual_value)
                raise TypeError(
                    f'The field `{f.name}` was assigned type `{current_type.__name__}` instead of `{expected_type.__name__}`')


class ReviewStatus(Enum):
    REVIEW_STATUS_UNSPECIFIED = 'REVIEW_STATUS_UNSPECIFIED'
    UNDER_REVIEW = 'UNDER_REVIEW'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    DRAFT = 'DRAFT'


class State(Enum):
    STATE_UNSPECIFIED = 'STATE_UNSPECIFIED'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'
    INACTIVE = 'INACTIVE'


class BarcodeType(Enum):
    BARCODE_TYPE_UNSPECIFIED = 'BARCODE_TYPE_UNSPECIFIED'
    AZTEC = 'AZTEC'
    CODE_39 = 'CODE_39'
    CODE_128 = 'CODE_128'
    CODABAR = 'CODABAR'
    DATA_MATRIX = 'DATA_MATRIX'
    EAN_8 = 'EAN_8'
    EAN_13 = 'EAN_13'
    ITF_14 = 'ITF_14'
    PDF_417 = 'PDF_417'
    QR_CODE = 'QR_CODE'
    UPC_A = 'UPC_A'
    TEXT_ONLY = 'TEXT_ONLY'


class BarcodeRenderEncoding(Enum):
    RENDER_ENCODING_UNSPECIFIED = 'RENDER_ENCODING_UNSPECIFIED'
    UTF_8 = 'UTF_8'


@dataclass
class EventTicketClassId(TypeCheckedDataclass):
    issuerId: str
    uniqueId: str


@dataclass
class EventTicketObjectId(TypeCheckedDataclass):
    issuerId: str
    uniqueId: str


@dataclass
class TranslatedString(TypeCheckedDataclass):
    language: str
    value: str


@dataclass
class LocalizedString(TypeCheckedDataclass):
    defaultValue: TranslatedString
    translatedValues: List[TranslatedString] = field(default_factory=list)


@dataclass
class ImageUri(TypeCheckedDataclass):
    uri: str


@dataclass
class Image(TypeCheckedDataclass):
    sourceUri: ImageUri
    contentDescription: Optional[LocalizedString] = None


@dataclass
class EventTicketClass(TypeCheckedDataclass):
    id: EventTicketClassId
    issuerName: str
    eventName: LocalizedString
    reviewStatus: ReviewStatus
    logo: Optional[Image] = None


@dataclass
class Barcode(TypeCheckedDataclass):
    type: BarcodeType
    renderEncoding: BarcodeRenderEncoding
    value: str
    alternateText: Optional[str] = None
    showCodeText: Optional[LocalizedString] = None


@dataclass
class EventTicketObject(TypeCheckedDataclass):
    id: EventTicketObjectId
    classId: EventTicketClassId
    state: State
    barcode: Optional[Barcode] = None


@dataclass
class EventTicketIdentifier(TypeCheckedDataclass):
    id: EventTicketObjectId
    classId: EventTicketClassId


@dataclass
class ObjectsToAddToWalet(TypeCheckedDataclass):
    eventTicketObjects: List[EventTicketIdentifier] = field(
        default_factory=list)


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
