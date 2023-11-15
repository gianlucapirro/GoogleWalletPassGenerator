from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import List, get_args, get_origin, Iterable, Optional
from collections.abc import Iterable
from .enums import ReviewStatus, State, BarcodeType, BarcodeRenderEncoding


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
