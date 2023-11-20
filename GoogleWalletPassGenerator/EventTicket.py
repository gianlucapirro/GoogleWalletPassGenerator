from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from google.auth import jwt, crypt
import json


class EventTicketManager:
    """Class for creating and managing Event tickets in Google Wallet."""

    def __init__(self, service_account_json: str):
        self.key_file_path = service_account_json
        self.base_url = 'https://walletobjects.googleapis.com/walletobjects/v1'
        self.class_url = f'{self.base_url}/eventTicketClass'
        self.object_url = f'{self.base_url}/eventTicketObject'

        self.auth()

    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.http_client = AuthorizedSession(self.credentials)
        print("Succesfully created http session")

    def create_class(self, event_ticket_class_data):
        """Create an EventTicketClass."""
        response = self.http_client.post(
            self.class_url, data=json.dumps(event_ticket_class_data))
        return response.json()

    def create_object(self, event_ticket_object_data):
        """Create an EventTicketObject."""
        response = self.http_client.post(
            self.object_url, data=json.dumps(event_ticket_object_data))
        return response.json()

    def create_add_event_ticket_urls(self, objects_to_add):
        """Create an add EventTicket to wallet link"""
        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['www.example.com'],
            'typ': 'savetowallet',
            'payload': objects_to_add
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        return f'https://pay.google.com/gp/v/save/{token}'
