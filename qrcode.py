import qrcode

data = "meet"
qr = qrcode.make(data)
qr.save("qrcode.png")
print("Qr Code Generated Successfully")