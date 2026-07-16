import sys

import smpplib.client
import smpplib.consts
from smpplib.command import Command
import traceback
import logging

# Activer les logs pour voir ce qui se passe
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
PASSWORD = "K4$hP4w"

def test_smpp_connection():
    client = None
    try:
        print(f"📡 Connexion à {HOST}:{PORT}")
        client = smpplib.client.Client(HOST, PORT)
        
        # Augmenter le timeout si possible
        # client.timeout = 30
        
        print("🔄 Établissement de la connexion TCP...")
        client.connect()
        print("✅ Connexion TCP établie")
        
        print("🔐 Authentification...")
        print(f"   System ID: {SYSTEM_ID}")
        client.bind_transceiver(
            system_id=SYSTEM_ID,
            password=PASSWORD
        )
        print("✅ Authentification réussie")
        
        print("📤 Envoi du message...")
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            source_addr="KashPaw",
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr="50948524055",
            short_message="Test SMS depuis KashPaw"
        )
        print("✅ Message envoyé!")
        print(f"   Sequence Number: {pdu.sequence if hasattr(pdu, 'sequence') else 'N/A'}")
        print(f"   PDU: {pdu}")
        
        return True
        
    except smpplib.exceptions.ConnectionError as e:
        print(f"❌ Erreur de connexion SMPP: {e}")
        print("   Causes possibles:")
        print("   - Le serveur a fermé la connexion")
        print("   - Timeout")
        print("   - Réseau instable")
        return False
        
    except smpplib.exceptions.SMPPError as e:
        print(f"❌ Erreur SMPP: {e}")
        print(f"   Code d'erreur: {getattr(e, 'code', 'N/A')}")
        return False
        
    except ConnectionRefusedError as e:
        print(f"❌ Connexion refusée: {e}")
        print("   Vérifiez que le serveur écoute sur le bon port")
        return False
        
    except TimeoutError as e:
        print(f"❌ Timeout: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print(f"   Type: {type(e).__name__}")
        print("\n📋 Traceback complet:")
        traceback.print_exc()
        return False
        
    finally:
        if client:
            try:
                print("🔄 Déconnexion...")
                client.unbind()
                client.disconnect()
                print("✅ Déconnecté")
            except Exception as e:
                print(f"⚠️ Erreur de déconnexion: {e}")

if __name__ == "__main__":
    success = test_smpp_connection()
    sys.exit(0 if success else 1)