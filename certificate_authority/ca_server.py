import pika
from os import path
import datetime

from OpenSSL.crypto import verify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from dotenv.main import load_dotenv
import os

load_dotenv()

CA_CERT_PATH = os.environ["CA_SELF_CERT"]
CA_KEY_PATH = os.environ["CA_PRIVATE_KEY"]


cert = None
key = None


def generate_or_load():
    global cert
    global key
    if (
        path.isfile(CA_CERT_PATH)
        and path.exists(CA_CERT_PATH)
        and path.isfile(CA_KEY_PATH)
        and path.exists(CA_KEY_PATH)
    ):
        # load files
        cert = x509.load_pem_x509_certificate(
            open(CA_CERT_PATH, "rb").read(), default_backend()
        )
        key = serialization.load_pem_private_key(
            open(CA_KEY_PATH, "rb").read(), password=None, backend=default_backend()
        )
    else:
        # generate key and self signed cert
        key = rsa.generate_private_key(
            public_exponent=65537, key_size=3072, backend=default_backend()
        )  # Save it to disk

        with open(CA_KEY_PATH, "wb") as f:
            f.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    # for programming reasons (no prompting)
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
            # Making a self signed certificate
        subject = issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "TN"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Tunis"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Insat"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "WeChat"),
                x509.NameAttribute(NameOID.COMMON_NAME, "WeChat"),
            ]
        )
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(
                # Our CA certificate will be valid for 9125 days ~ 25 years
                datetime.datetime.utcnow()
                + datetime.timedelta(days=9125)
            )
            .sign(key, hashes.SHA256(), default_backend())
        )
        # Write our certificate out to disk.
        with open(CA_CERT_PATH, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
    return (key, cert)


def handle_req(reqData, cert):
    csr = x509.load_pem_x509_csr(reqData, default_backend())
    cert_client = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=60))
    )
    for ext in csr.extensions:
        cert_client.add_extension(ext.value, ext.critical)

    cert_client = cert_client.sign(key, hashes.SHA256(), default_backend())
    return cert_client.public_bytes(serialization.Encoding.PEM).decode()


def handle_cert(data):
    if data:
        cert = x509.load_pem_x509_certificate(data, default_backend())
        return cert
    else:
        print("There is no certification")
        return None


class CaServer:
    def generate_authority_key(self):
        self.ca_key, self.ca_cert = generate_or_load()
        self.ca_pubkey = self.ca_key.public_key()

    def connect(self):
        self.generate_authority_key()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.receive()

    def send(self, client_queue, action, data):

        self.channel.exchange_declare(exchange="cert_exchange", exchange_type="direct")
        self.channel.queue_declare(queue=client_queue, durable=True)

        message = action + "::" + data
        self.channel.basic_publish(
            exchange="cert_exchange", routing_key=client_queue, body=message
        )

    def receive(self):
        self.channel.queue_declare(queue="cert_req_queue", durable=True)

        def callback(ch, method, properties, body):
            client_queue, action, data = body.decode().split("::")
            if action == "request":

                data = data.encode()
                certdata = handle_req(data, self.ca_cert)
                self.send(client_queue, "certif", certdata)
            if action == "verify":
                certif = handle_cert(data.encode())
                result = ""
                try:
                    result = self.ca_pubkey.verify(
                        certif.signature,
                        certif.tbs_certificate_bytes,
                        # Depends on the algorithm used to create the certificate
                        padding.PKCS1v15(),
                        certif.signature_hash_algorithm,
                    )
                    result = "Ok"
                except Exception:
                    result = "Not Verified"
                finally:
                    self.send(client_queue, "verify", result)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue="cert_req_queue", on_message_callback=callback)
        print("Server Started !! Listening")
        self.channel.start_consuming()


server = CaServer()
server.connect()
