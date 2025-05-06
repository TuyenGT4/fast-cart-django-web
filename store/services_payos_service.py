import hashlib
import hmac
import requests
from django.conf import settings

class PayOSService:
    def __init__(self):
        self.client_id = settings.PAYOS_CLIENT_ID
        self.api_key = settings.PAYOS_API_KEY
        self.checksum_key = settings.PAYOS_CHECKSUM_KEY
        self.endpoint = settings.PAYOS_ENDPOINT

    def _generate_checksum(self, params):
        sorted_params = ''.join(f"{key}{value}" for key, value in sorted(params.items()))
        checksum = hmac.new(
            self.checksum_key.encode('utf-8'),
            sorted_params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return checksum

    def initiate_payment(self, payment_data):
        url = f"{self.endpoint}/v2/payment-requests"
        headers = {
            "Content-Type": "application/json",
            "x-client-id": self.client_id,
            "x-api-key": self.api_key,
        }
        # PayOS v2 không cần checksum, chỉ gửi payload
        response = requests.post(url, json=payment_data, headers=headers)
        return response

    def validate_checksum(self, data):
        received_checksum = data.pop('checksum', '')
        generated_checksum = self._generate_checksum(data)
        return received_checksum == generated_checksum