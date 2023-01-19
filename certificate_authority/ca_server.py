from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid

from dotenv.main import load_dotenv
import os

load_dotenv()

CA_SELF_SERT=os.environ['CA_SELF_CERT']
CA_KEY=os.environ['CA_PRIVATE_KEY']

one_day = datetime.timedelta(1, 0, 0)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'WeChat'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'WeChatOrg'),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'WeChat unit'),
]))
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'WeChat'),
]))
builder = builder.not_valid_before(datetime.datetime.today() - one_day)
builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=100))
builder = builder.serial_number(int(uuid.uuid4()))
builder = builder.public_key(public_key)
builder = builder.add_extension(
    x509.BasicConstraints(ca=True, path_length=None), critical=True,
)
certificate = builder.sign(
    private_key=private_key, algorithm=hashes.SHA256(),
    backend=default_backend()
)
print(isinstance(certificate, x509.Certificate))

with open(CA_SELF_SERT, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"openstack-ansible")
    ))

with open(CA_KEY, "wb") as f:
    f.write(certificate.public_bytes(
        encoding=serialization.Encoding.PEM,
    ))