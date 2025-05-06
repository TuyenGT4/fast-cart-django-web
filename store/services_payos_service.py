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
        """
        Tạo checksum từ params và checksum key.
        """
        sorted_params = ''.join(f"{key}{value}" for key, value in sorted(params.items()))
        checksum = hmac.new(
            self.checksum_key.encode('utf-8'),
            sorted_params.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return checksum

    def initiate_payment(self, payment_data):
        """
        Gửi yêu cầu tới API PayOS để khởi tạo thanh toán.
        """
        url = f"{self.endpoint}/v1/payment/initiate"
        headers = {
            "Content-Type": "application/json",
            "X-Client-ID": self.client_id,
            "X-API-Key": self.api_key,
        }

        # Thêm checksum vào dữ liệu thanh toán
        payment_data['checksum'] = self._generate_checksum(payment_data)

        # Gửi yêu cầu tới API
        response = requests.post(url, json=payment_data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def validate_checksum(self, data):
        """
        Xác minh checksum từ dữ liệu callback.
        """
        checksum = data.pop('checksum', '')
        generated_checksum = self._generate_checksum(data)
        return checksum == generated_checksum

    def verify_payment(self, order_id):
        """
        Kiểm tra trạng thái thanh toán.
        """
        url = f"{self.endpoint}/v1/payment/status"
        headers = {
            "Content-Type": "application/json",
            "X-Client-ID": self.client_id,
            "X-API-Key": self.api_key,
        }
        payload = {"order_id": order_id}
        payload['checksum'] = self._generate_checksum(payload)

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()