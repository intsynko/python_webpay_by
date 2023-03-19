import hashlib
import unittest
from unittest.mock import patch
from unittest import mock

from webpay_be.client import WebpayClient


class TestWebpayClient(unittest.TestCase):
    def setUp(self):
        self.client = WebpayClient(
            is_test=True,
            option_3ds="disabled",
            store_id="123",
            store_name="My Store",
            version=1,
            language_id="en",
            url="https://api.example.com",
            secret_key="secret",
        )

    @patch("requests.post")
    def test_generate_payment(self, mock_post: mock.MagicMock):
        # Mock the response from the server
        response_data = {
            "data": {
                "transaction_id": "12345",
                "payment_url": "https://example.com/pay",
            }
        }
        mock_post.return_value.json.return_value = response_data
        mock_post.return_value.status_code = 200

        # Call the method being tested
        payment_data = self.client.generate_payment({"total": 12.34, "order_num": "123", "currency_id": "BYN"})

        # Assert that the request was made with the correct data
        expected_data = {
            "wsb_version": 1,
            "wsb_storeid": 123,
            "wsb_store": "My Store",
            "wsb_test": 1,
            "wsb_3ds_payment_option": "disabled",
            "wsb_language_id": "en",
            "wsb_total": 12.34,
            "wsb_order_num": "123",
            "wsb_currency_id": "BYN",
            "wsb_seed": mock.ANY,  # Check that a UUID is generated
            "wsb_signature": mock.ANY,  # Check that a signature is generated
        }
        mock_post.assert_called_once_with(
            url="https://api.example.com/api/v1/payment", json=expected_data
        )

        # Assert that the response is parsed correctly
        expected_payment_data = {
            "transaction_id": "12345",
            "payment_url": "https://example.com/pay",
        }
        self.assertEqual(payment_data, expected_payment_data)

        data = mock_post.call_args[1]['json']
        sign_key = f"{data['wsb_seed']}1231231BYN1234secret"
        self.assertEqual(data['wsb_signature'], hashlib.sha1(sign_key.encode()).hexdigest())

    def test_check_webhook_sign(self):
        webhook_data = {
            "batch_timestamp": "2022-03-21T11:22:33Z",
            "currency_id": "BYN",
            "amount": 99.99,
            "payment_method": "card",
            "order_id": "123",
            "site_order_id": "test123",
            "transaction_id": "456",
            "payment_type": "1",
            "rrn": "789",
            "card": "411111******1111"
        }

        # generate the expected signature
        sign_key = f"2022-03-21T11:22:33ZBYN9999card123test1234561789411111******1111secret"
        expected_signature = hashlib.sha1(sign_key.encode()).hexdigest()
        webhook_data["wsb_signature"] = expected_signature

        # check the signature
        self.assertTrue(self.client.check_webhook_sign(webhook_data))
        webhook_data["wsb_signature"] = 'incorrect_signature'
        self.assertFalse(self.client.check_webhook_sign(webhook_data))
