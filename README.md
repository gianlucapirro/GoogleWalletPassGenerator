# GoogleWalletPassGenerator

## Introduction

GoogleWalletPassGenerator is a Python package designed to simplify the process of creating passes for Google Wallet. This package provides an easy-to-use interface for generating various types of passes, including event tickets, boarding passes, loyalty cards, and more, compatible with Google Wallet.

## Features

-   Easy creation of Google Wallet passes.
-   Support for multiple pass types (event tickets, boarding passes, etc.).
-   Customizable pass templates.
-   Convenient serialization to JSON format compatible with Google Wallet API.

## Installation

To install GoogleWalletPassGenerator, run the following command:

```bash
pip install GoogleWalletPassGenerator
```

## Usage

Here is a basic example of how to create an EventTicket class

```python
from GoogleWalletPassGenerator.EventTicket import EventTicketManager
from GoogleWalletPassGenerator.Types import ReviewStatus, TranslatedString, LocalizedString, EventTicketClass, EventTicketClassId, EventTicketObject, EventTicketObjectId, State, Barcode, BarcodeType, BarcodeRenderEncoding, ObjectsToAdd, EventTicketIdentifier, serialize_to_json

service_account_json = 'path_to_service_account_json'
manager = EventTicketManager(service_account_json)

issuerId = 'ISSUER_ID'
uniqueClassId = 'UNIQUE_CLASS_ID'
uniqueObjectId = 'UNIQUE_OBJECT_ID'

eventTicketClass = serialize_to_json(
    EventTicketClass(
        id=EventTicketClassId(
            issuerId=issuerId,
            uniqueId=uniqueClassId
        ),
        issuerName="Crafture",
        eventName=LocalizedString(
            defaultValue=TranslatedString(
                "en-US", "EVENT_NAME"
            ),
            # Optionally add translations with translatedValues=[TranslatedString(), ...]
        ),
        reviewStatus=ReviewStatus.UNDER_REVIEW,  # Or any other status from the enum
    )
)

manager.create_class(eventTicketClass)
```

Here is a basic example of how to create an EventTicket Object of a class

```python
eventTicketObject = serialize_to_json(
    EventTicketObject(
        id=EventTicketObjectId(
            issuerId=issuerId,
            uniqueId=uniqueObjectId
        ),
        classId=EventTicketClassId(
            issuerId=issuerId,
            uniqueId=uniqueClassId
        ),
        state=State.ACTIVE,  # Or any other state from the enum
        barcode=Barcode(
            type=BarcodeType.QR_CODE,  # Or any other state from the enum
            renderEncoding=BarcodeRenderEncoding.UTF_8,  # Or any other state from the enum
            value="https://www.crafture.com/",
            # Optionally add alternateText and showCodeText
        )
    )
)

manager.create_object(eventTicketObject)
```

You can now create the add to Google Wallet urls:

```python
objectsToAdd = serialize_to_json(
    ObjectsToAddToWalet(
        [
            EventTicketIdentifier(
                id=EventTicketObjectId(
                    issuerId=issuerId,
                    uniqueId=uniqueObjectId
                ),
                classId=EventTicketClassId(
                    issuerId=issuerId,
                    uniqueId=uniqueClassId
                ),
            )
        ]
    )
)

walletUrls = manager.create_add_event_ticket_urls(objectsToAdd)
print(walletUrls)
```
