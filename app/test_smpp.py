#!/usr/bin/env python3
import socket
import subprocess
import sys
import smpplib.client
import smpplib.consts

HOST = "172.20.222.38"
PORT = 5020

def diagnose_connection():
    print("=" * 60)
    print("DIAGNOSTIC DE CONNEXION SMPP")
    print("=" * 60)
    
    # 1. Tester la résolution DNS
    print(f"\n1. Résolution DNS de {HOST}")
    try:
        ip = socket.gethostbyname(HOST)
        print(f"   ✅ Résolu: {ip}")
    except Exception as e:
        print(f"   ❌ Erreur DNS: {e}")
        return False
    
    # 2. Tester le port
    print(f"\n2. Test du port {PORT}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((HOST, PORT))
        sock.close()
        
        if result == 0:
            print(f"   ✅ Port {PORT} ouvert")
        else:
            print(f"   ❌ Port {PORT} fermé ou filtré (code: {result})")
            print(f"   Vérifiez avec: nc -zv {HOST} {PORT}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # 3. Tester avec telnet/nc
    print(f"\n3. Test de connexion avec netcat")
    try:
        result = subprocess.run(
            ['nc', '-zv', '-w', '2', HOST, str(PORT)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"   ✅ Connexion possible")
        else:
            print(f"   ⚠️ Netcat: {result.stderr.strip()}")
    except FileNotFoundError:
        print("   ⚠️ netcat non disponible")
    
    print("\n" + "=" * 60)
    return True

# Exécuter le diagnostic
if not diagnose_connection():
    print("\n❌ Diagnostic échoué. Corrigez les problèmes ci-dessus.")
    sys.exit(1)

# Tenter la connexion SMPP
print("\n🔌 Tentative de connexion SMPP...")
SYSTEM_ID = "KASHPAW"
PASSWORD = "K4$hP4w"

client = smpplib.client.Client(HOST, PORT)

try:
    client.connect()
    print("✅ Connecté au serveur SMPP")
    
    client.bind_transceiver(
        system_id=SYSTEM_ID,
        password=PASSWORD
    )
    print("✅ Bind réussi")
    
    # Envoyer un message test
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
    print("\nCauses possibles:")
    print("- Le serveur SMPP n'est pas démarré")
    print("- Le firewall bloque la connexion")
    print("- Adresse IP ou port incorrect")
    
except smpplib.exceptions.BindError as e:
    print(f"❌ Erreur d'authentification: {e}")
    print("\nCauses possibles:")
    print("- System_id ou password incorrect")
    print("- Le compte n'a pas les permissions")
    print("- Le serveur est en mode lecture seule")
    
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
    
finally:
    try:
        client.unbind()
        client.disconnect()
    except:
        pass