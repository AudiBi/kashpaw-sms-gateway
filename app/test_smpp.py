import smpplib.client
import smpplib.consts
from smpplib.command import Command

# ===== PATCH POUR CORRIGER LE BUG DE CONCATÉNATION =====
def _generate_string_patched(self, field):
    """Generate PDU string field - version corrigée."""
    field_value = getattr(self, field)
    if field_value is None:
        return b''
    # Convertir en bytes si nécessaire
    if isinstance(field_value, str):
        field_value = field_value.encode('utf-8')
    elif not isinstance(field_value, bytes):
        field_value = str(field_value).encode('utf-8')
    # Ajouter le terminateur null en bytes
    return field_value + b'\x00'

# Appliquer le patch
Command._generate_string = _generate_string_patched
# ========================================================

HOST = "172.20.222.38"
PORT = 5020

SYSTEM_ID = "......"
PASSWORD = "....."

client = smpplib.client.Client(HOST, PORT)

try:
    client.connect()
    print("✅ Connecté au serveur SMPP")
    
    client.bind_transceiver(
        system_id=SYSTEM_ID,
        password=PASSWORD
    )
    print("✅ Bind réussi")
    
    # Envoyer le message - Les paramètres peuvent être en string
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
        source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
        source_addr="KashPaw",
        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        destination_addr="50948524055",
        short_message="Test SMPP"
    )
    print(f"✅ Message envoyé avec succès!")
    print(f"   PDU: {pdu}")
    
    client.unbind()
    client.disconnect()
    print("✅ Déconnecté")
    
except smpplib.exceptions.ConnectionError as e:
    print(f"❌ Erreur de connexion: {e}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    
finally:
    try:
        client.unbind()
        client.disconnect()
    except:
        pass