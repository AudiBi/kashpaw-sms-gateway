import smpplib.client
import smpplib.consts
from smpplib.command import Command

# Patch pour corriger le bug de concaténation
def _generate_string_patched(self, field):
    """Generate PDU string field."""
    field_value = getattr(self, field)
    if field_value is None:
        return b''
    # Convertir en bytes si ce n'est pas déjà fait
    if isinstance(field_value, str):
        field_value = field_value.encode('utf-8')
    # Ajouter le terminateur null en bytes
    return field_value + b'\x00'

# Appliquer le patch
Command._generate_string = _generate_string_patched

HOST = "172.20.222.38"
PORT = 5020

SYSTEM_ID = "KASHPAW"
PASSWORD = "K4$hP4w"

client = smpplib.client.Client(HOST, PORT)
client.connect()
client.bind_transceiver(
    system_id=SYSTEM_ID,
    password=PASSWORD
)

print("Bind OK")

pdu = client.send_message(
    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
    source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
    source_addr="KashPaw",  # Peut rester en string maintenant
    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
    destination_addr="50948524055",  # Peut rester en string
    short_message="Test SMPP"  # Peut rester en string
)

print(pdu)

client.unbind()
client.disconnect()