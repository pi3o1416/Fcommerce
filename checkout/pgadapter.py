
import requests

from django.conf import settings
from .exceptions import FailedToInitiatePayment


class PGAdapter:
    def __init__(self, order):
        self.order = order

    def initiate_payment(self):
        url = settings.PG_PAYMENT_INITIATE_URL
        request_data = self.generate_request_body()
        response = requests.post(
            url=url,
            json=request_data
        )
        # Result will be only available if successfully generate a payment url since 200 is common status code
        if response.status_code == 200 and 'result' in response.json():
            return response.json()
        elif response.status_code == 200:
            raise FailedToInitiatePayment(detail=response.json())
        raise FailedToInitiatePayment(detail="PG Server Error")

    def generate_request_body(self):
        merchant = self.order.merchant
        request_body = {
            "store_id": merchant.merchant_id,
            "signature_key": merchant.signature_key,
            "tran_id": str(self.order.transaction_id),
            "amount": str(self.order.total_amount),
            "currency": str(self.order.payment_currency),
            "desc": self.order.description,
            "cus_name": self.order.customer_name,
            "cus_email": self.order.customer_email,
            "cus_phone": self.order.customer_phone_no,
            "success_url": merchant.success_url,
            "fail_url": merchant.failed_url,
            "cancel_url": merchant.cancel_url,
            "type": "json"
        }
        return request_body
