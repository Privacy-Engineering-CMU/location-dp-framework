from flask import Flask, request, jsonify
import io
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

app = Flask(__name__)


@app.route('/process-data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        part1_bytes = request.files['part1'].read()
        part2_bytes = request.files['part2'].read()


        decrypted_data = private_key.decrypt(
            part1_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        part1_data = io.BytesIO(part1_bytes)
        part2_data = io.BytesIO(part2_bytes)


        return 'Data processed successfully!'
    else:
        return 'Only POST requests are supported.'


# Generate a private key (Do this once and store securely)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()


@app.route('/get-public-key')
def get_public_key():
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return jsonify({'public_key': pem.decode('utf-8')})


if __name__ == '__main__':
    app.run(debug=True)
