from flask import Flask, request, jsonify
import io
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

app = Flask(__name__)


class Leader():
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.data_list = []

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def add(self, data):
        return self.data_list.append(data)

    def decrypt(self, data):
        self.data_list.append(self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        )
        return 'Data processed successfully!'


class Helper():
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def decrypt(self, data):
        return self.private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


leader = Leader()
helper = Helper()


@app.route('/process-data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        part1_bytes = request.files['part1'].read()
        part2_bytes = request.files['part2'].read()

        part1_decrypted_data = leader.decrypt(
            part1_bytes
        )

        part2_decrypted_data = helper.decrypt(
            part2_bytes
        )

        return 'Data processed successfully!'
    else:
        return 'Only POST requests are supported.'


@app.route('/get-public-key')
def get_public_key():
    resp = {
        "pk1": {'public_key': leader.get_public_key().decode('utf-8')},
        "pk2": {'public_key': helper.get_public_key().decode('utf-8')}
    }

    return jsonify(resp)


@app.route('/admin/aggregate')
def aggregate():
    resp = {
        "data": leader.data_list
    }
    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)
