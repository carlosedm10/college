import os
import pyotp
import base64
from generate_qr import get_QR

DNI = os.getenv("DNI")


# Encode the DNI and convert it to a string
secret = base64.b32encode(bytearray(DNI, "ascii")).decode("utf-8")
print("Mi secreto:", secret)  # Print the generated secret

# Create a TOTP (Time-based One-Time Password) object using the generated secret
totp_object = pyotp.TOTP(secret)

# Generate a provisioning URI for the QR code, which can be used by an app like Google Authenticator
qr_text = totp_object.provisioning_uri(name="mi_usuario", issuer_name="Mi App")

# Print the URI text, which can be used to generate a QR code for setting up two-factor authentication
print(qr_text)

get_QR(qr_text)

otp = input("ingresa el código OTP:")
valid = totp_object.verify(totp_object)
print(valid)
