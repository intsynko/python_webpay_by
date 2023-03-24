import hashlib
import uuid

import requests


class WebpayClient:
    class PaymentType:
        Completed = 1
        Declined = 2
        Pending = 3
        Authorized = 4
        PartialRefunded = 5
        System = 6
        Voided = 7
        Failed = 8
        PartialVoided = 9
        Recurrent = 10
        Refunded = 11

    def __init__(self, is_test: bool, option_3ds: str, store_id: str, store_name: str,
                 version: int, language_id: str, url: str, secret_key: str):
        self.is_test = is_test
        self.option_3ds = option_3ds
        self.store_id = store_id
        self.store_name = store_name
        self.version = version
        self.language_id = language_id
        self.url = url
        self.secret_key = secret_key

    def _process_float_for_sign(self, num):
        if num == int(num):
            return str(int(num))
        return str(num)

    def _get_sign_key_for_webhook(self, data):
        fields_to_sign = [
            str(data["batch_timestamp"]),
            data["currency_id"],
            data["amount"],
            data["payment_method"],
            data["order_id"],
            data["site_order_id"],
            data["transaction_id"],
            data["payment_type"],
            data["rrn"],
        ]
        if data.get("card"):
            fields_to_sign.append(data["card"])
        fields_to_sign.append(self.secret_key)
        return "".join(fields_to_sign)

    def check_webhook_sign(self, data):
        sign_key = self._get_sign_key_for_webhook(data)
        return data["wsb_signature"] == hashlib.md5(sign_key.encode()).hexdigest()

    def _get_sign_key(self, data: dict):
        return "".join([data["seed"],
                        str(self.store_id),
                        data["order_num"],
                        str(data["test"]),
                        data["currency_id"],
                        self._process_float_for_sign(data["total"]),
                        self.secret_key])

    def _prepare_data(self, data):
        return {
            "version": self.version,  # webpay api version
            "storeid": int(self.store_id),
            "store": self.store_name,
            "test": 1 if self.is_test else 0,
            "3ds_payment_option": self.option_3ds,
            "language_id": self.language_id,
            **data,
            "seed": str(uuid.uuid4()),
        }

    def generate_payment(self, data: dict):
        data = self._prepare_data(data)
        sign_key = self._get_sign_key(data)
        data["signature"] = hashlib.sha1(sign_key.encode()).hexdigest()
        data['total'] = float(data['total'])
        data['invoice_item_price'] = [float(item) for item in data['invoice_item_price']]
        data = {f"wsb_{k}": v for k,v in data.items()}
        response = requests.post(url=f"{self.url}/api/v1/payment", json=data)
        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"{e}, response: {response.json()}, request: {data}")
        return response.json()["data"]
