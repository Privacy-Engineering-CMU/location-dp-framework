import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# ... Assuming you've fetched the server's public key ...
server_public_key_pem = """-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"""


def get_public_key():

    data = []

    response = requests.get(
        'http://127.0.0.1:5000/get-public-key',
    )

    if response.status_code == 200:
        global server_public_key_pem
        server_public_key_pem = response
    else:
        print('An error occurred.')


def encrypt_and_send_data(data, server_public_key_pem):
    public_key = serialization.load_pem_public_key(server_public_key_pem.encode())
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    response = requests.post(
        'http://127.0.0.1:5000/process-data',
        data=encrypted_data
    )

    if response.status_code == 200:
        print('Data encrypted and sent successfully.')
    else:
        print('An error occurred.')

# Example Usage
data_to_send = b'This is some important data to encrypt.'
encrypt_and_send_data(data_to_send, server_public_key_pem)