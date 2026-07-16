import socket
import binascii
import time
import struct

HOST = "172.20.222.38"
PORT = 5020
SYSTEM_ID = "KASHPAW"
PASSWORD = "K4h$p4w"  # Remplacez par votre vrai mot de passe

def test_manual_bind():
    """Test manuel de bind pour voir la réponse du serveur."""
    print("=" * 60)
    print("TEST MANUAL BIND")
    print("=" * 60)
    
    try:
        # Connexion TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((HOST, PORT))
        print("✅ Connexion TCP établie")
        
        # Construction de la PDU bind_transmitter
        # Command ID: 0x00000002 (bind_transmitter)
        # Status: 0x00000000
        # Sequence: 0x00000001
        
        # Encoder les champs
        system_id_bytes = SYSTEM_ID.encode('ascii') + b'\x00'
        password_bytes = PASSWORD.encode('ascii') + b'\x00'
        system_type = b'\x00'
        interface_version = b'\x34'  # SMPP 3.4
        addr_ton = b'\x00'
        addr_npi = b'\x00'
        address_range = b'\x00'
        
        # Calculer la longueur totale
        body = (
            system_id_bytes +
            password_bytes +
            system_type +
            interface_version +
            addr_ton +
            addr_npi +
            address_range
        )
        command_length = 16 + len(body)  # 16 = header length
        
        # Construire l'en-tête
        header = struct.pack('>IIII', command_length, 0x00000002, 0x00000000, 0x00000001)
        pdu = header + body
        
        print(f"\n📤 Envoi de la PDU bind_transmitter:")
        print(f"   Longueur: {command_length}")
        print(f"   Hex: {binascii.hexlify(pdu).decode()}")
        
        sock.send(pdu)
        print("✅ PDU envoyée")
        
        # Attendre la réponse
        print("\n⏳ Attente de la réponse du serveur...")
        response = sock.recv(1024)
        
        if response:
            print(f"✅ Réponse reçue ({len(response)} bytes)")
            print(f"   Hex: {binascii.hexlify(response).decode()}")
            
            # Décoder la réponse
            if len(response) >= 16:
                cmd_len, cmd_id, cmd_status, seq = struct.unpack('>IIII', response[:16])
                print(f"\n📥 Décodage de la réponse:")
                print(f"   Longueur: {cmd_len}")
                print(f"   Command ID: 0x{cmd_id:08x}")
                print(f"   Status: 0x{cmd_status:08x}")
                print(f"   Sequence: {seq}")
                
                if cmd_status == 0x00000000:
                    print("   ✅ Status: SUCCESS")
                else:
                    print(f"   ❌ Status: ERROR (0x{cmd_status:08x})")
                    
                    # Erreurs communes
                    errors = {
                        0x00000001: "SMPP_ESME_RINVMSGLEN - Invalid message length",
                        0x0000000A: "SMPP_ESME_RINVSYSID - Invalid System ID",
                        0x0000000E: "SMPP_ESME_RINVPASWD - Invalid Password",
                        0x0000000F: "SMPP_ESME_RINVBNDSTS - Bind failed",
                        0x00000014: "SMPP_ESME_RBINDFAIL - Binding failed",
                    }
                    if cmd_status in errors:
                        print(f"   Explication: {errors[cmd_status]}")
        else:
            print("❌ Aucune réponse du serveur")
            
    except socket.timeout:
        print("❌ Timeout - Le serveur ne répond pas")
        print("   Le serveur a reçu la PDU mais ne répond pas")
        
    except ConnectionRefusedError:
        print("❌ Connexion refusée")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        try:
            sock.close()
            print("\n🔌 Socket fermé")
        except:
            pass

def test_smpp_connection():
    """Test avec smpplib avec plus de détails."""
    print("\n" + "=" * 60)
    print("TEST SMPPLIB")
    print("=" * 60)
    
    import smpplib.client
    import smpplib.consts
    from smpplib.command import Command
    
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
    
    client = smpplib.client.Client(HOST, PORT)
    
    try:
        client.connect()
        print("✅ Connecté")
        
        # Essayer avec des paramètres plus complets
        print("\n🔐 Tentative de bind_transmitter...")
        client.bind_transmitter(
            system_id=SYSTEM_ID,
            password=PASSWORD,
            system_type='',
            interface_version=0x34,
            addr_ton=0,
            addr_npi=0,
            address_range=''
        )
        print("✅ Bind réussi!")
        
        print("\n📤 Envoi du message...")
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            source_addr="KashPaw",
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr="50948524055",
            short_message="Test SMS",
            esm_class=0,
            data_coding=0,
            priority_flag=0,
            registered_delivery=0,
            replace_if_present_flag=0
        )
        print("✅ Message envoyé avec succès!")
        print(f"   Sequence: {pdu.sequence}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        
    finally:
        try:
            client.unbind()
            client.disconnect()
            print("✅ Déconnecté")
        except:
            pass

def test_with_timeout():
    """Test avec différents timeouts."""
    print("\n" + "=" * 60)
    print("TEST AVEC TIMEOUT")
    print("=" * 60)
    
    import smpplib.client
    from smpplib.command import Command
    
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
    
    # Test avec différents timeouts
    for timeout in [5, 10, 20, 30]:
        print(f"\n⏱️ Test avec timeout de {timeout} secondes")
        
        try:
            client = smpplib.client.Client(HOST, PORT)
            # Si la version supporte le timeout
            if hasattr(client, 'timeout'):
                client.timeout = timeout
            
            client.connect()
            print("   ✅ Connecté")
            
            client.bind_transmitter(
                system_id=SYSTEM_ID,
                password=PASSWORD
            )
            print(f"   ✅ Bind réussi avec timeout {timeout}")
            
            client.unbind()
            client.disconnect()
            break
            
        except smpplib.exceptions.ConnectionError:
            print(f"   ❌ Erreur de connexion avec timeout {timeout}")
            
        except Exception as e:
            print(f"   ❌ Erreur avec timeout {timeout}: {e}")
            
        finally:
            try:
                client.unbind()
                client.disconnect()
            except:
                pass

if __name__ == "__main__":
    # 1. D'abord, tester manuellement
    test_manual_bind()
    
    # 2. Puis tester avec smpplib
    test_smpp_connection()
    
    # 3. Enfin, tester avec différents timeouts
    test_with_timeout()