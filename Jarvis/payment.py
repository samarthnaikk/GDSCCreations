#This file has no use in the mainfile, but is an upcoming feature of the bot. File is not complete and its creation is under progress

import razorpay
import qrcode
import time

RAZORPAY_KEY_ID = "your_key"
RAZORPAY_KEY_SECRET = "razor_pay_key"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_order(amount):
    try:
        order_data = {
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": 1
        }
        order = client.order.create(order_data)
        return order["id"]
    except Exception as e:
        print(f"Error creating order: {e}")
        return None

def generate_payment_qr(order_id, upi_id, amount, filename="upi_qr.png"):
    upi_link = f"upi://pay?pa={upi_id}&pn=your_name&am={amount}&cu=INR&tid={order_id}"
    qr = qrcode.make(upi_link)
    qr.save(filename)
    return filename

def check_payment(order_id, expected_amount):
    try:
        payments = client.order.payments(order_id)
        
        for payment in payments["items"]:
            if payment["status"] == "captured" and float(payment["amount"]) / 100 == expected_amount:
                print(f"Payment received! Payment ID: {payment['id']}")
                return True
        
        print("Payment not yet completed...")
        return False
    except Exception as e:
        print(f"Error checking payment: {e}")
        return False

def wait_for_payment(order_id, amount, timeout=300, interval=10):
    elapsed = 0
    while elapsed < timeout:
        if check_payment(order_id, amount):
            return True
        time.sleep(interval)
        elapsed += interval

    print("Payment timeout reached.")
    return False
amount = 1.0
upi_id = "your_upi_id"

order_id = create_order(amount)
if order_id:
    qr_filename = generate_payment_qr(order_id, upi_id, amount)
    print(f"QR Code saved as {qr_filename}")

if order_id:
    if wait_for_payment(order_id, amount):
        print("Payment received successfully!")
    else:
        print("Payment not received in time.")
