import smpplib.client
import smpplib.consts
from smpplib.command import Command
import logging

# Activer les logs si nécessaire
# logging.basicConfig(level=logging.DEBUG)

# ===== PATCH =====
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
# =================

HOST = "172.20.222.38"
PORT = 5020
SYSTEM_ID = "KASHPAW"
PASSWORD = "K4$hP4w"  # <-- METTEZ LE BON MOT DE PASSE

def send_sms(destination, message, source="KashPaw"):
    """Envoyer un SMS via SMPP."""
    client = None
    try:
        client = smpplib.client.Client(HOST, PORT)
        client.connect()
        print("✅ Connecté au serveur SMPP")
        
        client.bind_transmitter(
            system_id=SYSTEM_ID,
            password=PASSWORD
        )
        print("✅ Authentification réussie")
        
        # Envoyer le message
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            source_addr=source,
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr=destination,
            short_message=message,
            esm_class=0,
            data_coding=0
        )
        
        print(f"✅ Message envoyé avec succès!")
        print(f"   A: {destination}")
        print(f"   Message: {message}")
        print(f"   Sequence: {pdu.sequence}")
        
        return True
        
    except smpplib.exceptions.ConnectionError as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
        
    finally:
        if client:
            try:
                client.unbind()
                client.disconnect()
                print("✅ Déconnecté")
            except:
                pass

if __name__ == "__main__":
    # Envoyer un SMS
    success = send_sms(
        destination="50948524055",
        message="Test SMS depuis KashPaw"
    )
    
    if success:
        print("\n✅ SMS envoyé avec succès !")
    else:
        print("\n❌ Échec de l'envoi du SMS")