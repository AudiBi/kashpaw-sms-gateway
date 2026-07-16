import smpplib.client
import smpplib.consts
from smpplib.command import Command
import time

# Patch
def _generate_string_patched(self, field):
    field_value = getattr(self, field)
    if field_value is None:
        return b''
    if isinstance(field_value, str):
        field_value = field_value.encode('utf-8')
    elif not isinstance(field_value, bytes):
        field_value = str(field_value).encode('utf-8')
    return field_value + b'\x00'

Command._generate_string = _generate_string_patched

HOST = "172.20.222.38"
PORT = 5020
SYSTEM_ID = "KASHPAW"  # Majuscules comme dans le debug
PASSWORD = "K4h$p4w"   # Utilisez le bon mot de passe

client = smpplib.client.Client(HOST, PORT)

try:
    client.connect()
    print("✅ Connecté")
    
    # Essayer avec bind_transmitter au lieu de bind_transceiver
    print("🔐 Tentative d'authentification en mode Transmitter...")
    client.bind_transmitter(
        system_id=SYSTEM_ID,
        password=PASSWORD
    )
    print("✅ Bind Transmitter réussi")
    
    # Envoyer le message
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
        source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
        source_addr="KashPaw",
        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        destination_addr="50948524055",
        short_message="Test SMS"
    )
    print(f"✅ Message envoyé: {pdu}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    try:
        client.unbind()
        client.disconnect()
    except:
        pass