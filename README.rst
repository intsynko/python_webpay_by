Python client for webpay.by json api
========================

Python client for webpay Belorussia: https://docs.webpay.by/payment-json.html#operation/paymentReq 

Install
-------

``pip install git+https://github.com/intsynko/python_webpay_by@master``

How to use
------------
.. code:: python

    from webpay_by.client import WebpayClient

    SANBOX = 'https://securesandbox.webpay.by'
    secret_key = 'secret_key'

    cilent = WebpayClient(is_test=True, option_3ds="auto", store_id="123", store_name="Your shop display name",
                          version=2, language_id="russian", secret_key=secret_key, secret_key=SANBOX)

    resopnse = client.generate_payment(**{
        "return_url": "https://example.com/succees_url",
        "cancel_return_url": "https://example.com/fail_url",
        "notify_url": "https://example.com/webhook/", # optional
        "order_num": "123",
        "currency_id": "BYN",
        "invoice_itemname": ["a", "b"],
        "invoice_item_quantity": [1,2],
        "invoice_item_price": [4.0, 6.0],
        "total": "10",
        "customer_name": "client name (will be displayed in payment form)", # optional
        "email": "client@mail.by",
        ... # other optional params from documentation
    })

    redirect_url = resopnse["redirectUrl"]

