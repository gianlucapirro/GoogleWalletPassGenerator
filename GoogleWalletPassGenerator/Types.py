from dataclasses import dataclass, field, asdict, fields, is_dataclass
from typing import List, get_args, get_origin, Iterable, Optional
from collections.abc import Iterable
from .enums import ReviewStatus, State, BarcodeType, BarcodeRenderEncoding, DoorsOpenLabel, MultipleDevicesAndHoldersAllowedStatus, ViewUnlockRequirement, MessageType, TotpAlgorithm, ScreenshotEligibility, NfcConstraint


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
                        f'WRONG TYPE: Items in field `{f.name}` are not of type `{item_type.__name__}`')
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
class Barcode(TypeCheckedDataclass):
    type: BarcodeType
    renderEncoding: BarcodeRenderEncoding
    value: str
    alternateText: Optional[str] = None
    showCodeText: Optional[LocalizedString] = None


@dataclass
class EventVenue(TypeCheckedDataclass):
    name: LocalizedString
    address: LocalizedString


@dataclass
class EventDateTime(TypeCheckedDataclass):
    doorsOpen: str
    start: str
    end: str
    doorsOpenLabel: Optional[DoorsOpenLabel] = None
    customDoorsOpenLabel: Optional[LocalizedString] = None


@dataclass
class Uri(TypeCheckedDataclass):
    uri: str
    description: Optional[str] = None
    localizedDescription: Optional[LocalizedString] = None
    id: Optional[str] = None


@dataclass
class LatLongPoint(TypeCheckedDataclass):
    latitude: float
    longitude: float


@dataclass
class Review(TypeCheckedDataclass):
    comments: str


@dataclass
class ImageModuleData(TypeCheckedDataclass):
    mainImage: Image
    id: str


@dataclass
class TextModuleData(TypeCheckedDataclass):
    header: str
    body: str
    localizedHeader: Optional[LocalizedString] = None
    localizedBody: Optional[LocalizedString] = None
    id: Optional[str] = None


@dataclass
class LinksModuleData(TypeCheckedDataclass):
    uris: List[Uri] = field(default_factory=list)


@dataclass
class CallbackOptions(TypeCheckedDataclass):
    url: str
    updateRequestUrl: str


@dataclass
class EventTicketClass(TypeCheckedDataclass):
    id: EventTicketClassId
    issuerName: str
    eventName: LocalizedString
    reviewStatus: ReviewStatus
    logo: Optional[Image] = None
    version: Optional[str] = None
    venue: Optional[EventVenue] = None
    dateTime: Optional[EventDateTime] = None
    customSeatLabel: Optional[LocalizedString] = None
    customRowLabel: Optional[LocalizedString] = None
    customSectionLabel: Optional[LocalizedString] = None
    customGateLabel: Optional[LocalizedString] = None
    finePrint: Optional[LocalizedString] = None
    homepageUri: Optional[Uri] = None
    locations: List[LatLongPoint] = field(default_factory=list)
    review: Optional[Review] = None
    imageModuleData: List[ImageModuleData] = field(default_factory=list)
    textModuleData: List[TextModuleData] = field(default_factory=list)
    linksModuleData: Optional[LinksModuleData] = None
    countryCode: Optional[str] = None
    heroImage: Optional[Image] = None
    hexBackgroundColor: Optional[str] = None
    localizedIssuerName: Optional[LocalizedString] = None
    multipleDevicesAndHoldersAllowedStatus: Optional[MultipleDevicesAndHoldersAllowedStatus] = None
    callbackOptions: Optional[CallbackOptions] = None
    viewUnlockRequirement: Optional[ViewUnlockRequirement] = None
    wideLogo: Optional[Image] = None


@dataclass
class EventSeat(TypeCheckedDataclass):
    seat: Optional[LocalizedString] = None
    row: Optional[LocalizedString] = None
    section: Optional[LocalizedString] = None
    gate: Optional[LocalizedString] = None


@dataclass
class EventReservationInfo(TypeCheckedDataclass):
    confirmationCode: str


@dataclass
class Money(TypeCheckedDataclass):
    micros: str
    currencyCode: str


@dataclass
class GroupingInfo(TypeCheckedDataclass):
    sortIndex: int
    groupingId: str


@dataclass
class DateTime(TypeCheckedDataclass):
    date: str


@dataclass
class TimeInterval(TypeCheckedDataclass):
    start: DateTime
    end: DateTime


@dataclass
class Message(TypeCheckedDataclass):
    header: str
    body: str
    messageType: MessageType
    displayInterval: TimeInterval
    id: Optional[str] = None
    localizedHeader: Optional[LocalizedString] = None
    localizedBody: Optional[LocalizedString] = None


@dataclass
class AppTarget(TypeCheckedDataclass):
    targetUri: Uri


@dataclass
class AppLinkInfo(TypeCheckedDataclass):
    title: LocalizedString
    description: LocalizedString
    appTarget: AppTarget
    appLogoImage: Optional[Image] = None


@dataclass
class AppLinkData(TypeCheckedDataclass):
    androidAppLinkInfo: Optional[AppLinkInfo] = None
    iosAppLinkInfo: Optional[AppLinkInfo] = None
    webAppLinkInfo: Optional[AppLinkInfo] = None


@dataclass
class TotpParameters(TypeCheckedDataclass):
    key: str
    valueLength: str


@dataclass
class TotpDetails(TypeCheckedDataclass):
    periodMillis: str
    algorithm: TotpAlgorithm
    parameters: List[TotpParameters] = field(default_factory=list)


@dataclass
class RotatingBarcodeValues(TypeCheckedDataclass):
    startDateTime: str
    periodMillis: str
    values: List[str] = field(default_factory=list)


@dataclass
class RotatingBarcode(TypeCheckedDataclass):
    type: BarcodeType
    renderEncoding: BarcodeRenderEncoding
    valuePattern: str
    totpDetails: TotpDetails
    alternateText: Optional[str] = None
    showCodeText: Optional[LocalizedString] = None
    initialRotatingBarcodeValues = RotatingBarcodeValues


@dataclass
class PassConstraints(TypeCheckedDataclass):
    screenshotEligibility: ScreenshotEligibility
    nfcConstraint: NfcConstraint


@dataclass
class EventTicketObject(TypeCheckedDataclass):
    id: EventTicketObjectId
    classId: EventTicketClassId
    state: State
    barcode: Optional[Barcode] = None
    classReference: Optional[EventTicketClass] = None
    seatInfo: Optional[EventSeat] = None
    reservationInfo: Optional[EventReservationInfo] = None
    ticketHolderName: Optional[str] = None
    ticketNumber: Optional[str] = None
    ticketType: Optional[LocalizedString] = None
    faceValue: Optional[Money] = None
    groupingInfo: Optional[GroupingInfo] = None
    linkedOfferIds: Optional[str] = None
    hexBackgroundColor: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    validTimeInterval: Optional[TimeInterval] = None
    locations: List[LatLongPoint] = field(default_factory=list)
    hasUsers: Optional[bool] = None
    hasLinkedDevice: Optional[bool] = None
    disableExpirationNotification: Optional[bool] = None
    imageModuleData: List[ImageModuleData] = field(default_factory=list)
    textModuleData: List[TextModuleData] = field(default_factory=list)
    linksModuleData: Optional[LinksModuleData] = None
    appLinkData: Optional[AppLinkData] = None
    rotatingBarcode: Optional[RotatingBarcode] = None
    heroImage: Optional[Image] = None
    passConstraints: Optional[PassConstraints] = None


@dataclass
class EventTicketIdentifier(TypeCheckedDataclass):
    id: EventTicketObjectId
    classId: EventTicketClassId


@dataclass
class ObjectsToAddToWallet(TypeCheckedDataclass):
    eventTicketObjects: List[EventTicketIdentifier] = field(
        default_factory=list)
