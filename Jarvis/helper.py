import qrcode

def generate_upi_qr(upi_id, amount, filename="upi_qr.png"):
    upi_link = f"upi://pay?pa={upi_id}&pn=your_name&am={amount}&cu=INR"
    qr = qrcode.make(upi_link)
    qr.save(filename)
    return filename

generate_upi_qr("recievers upi id", 1.5)
