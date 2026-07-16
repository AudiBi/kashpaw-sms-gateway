#!/usr/bin/env python3

import traceback
import smpplib.client
import smpplib.consts
import smpplib.gsm

# ==========================
# CONFIGURATION
# ==========================

HOST = "172.20.222.38"
PORT = 5020

SYSTEM_ID = "KASHPAW"
PASSWORD = "K4$hP4w"

DESTINATION = "50948524055"

# Commencez avec un numéro comme source.
# Si Digicel autorise un Sender ID alphanumérique,
# nous le changerons ensuite.
SOURCE_ADDR = "KashPaw"

# ==========================
# CONNEXION
# ==========================

client = smpplib.client.Client(HOST, PORT)

client.set_message_received_handler(
    lambda pdu, **kwargs: print("DeliverSM:", pdu)
)

try:

    print("=" * 60)
    print("Connexion au serveur SMPP...")
    print("=" * 60)

    client.connect()

    print("Connexion TCP OK")

    print("\nBind Transceiver...")

    client.bind_transceiver(
        system_id=SYSTEM_ID,
        password=PASSWORD
    )

    print("✅ Bind réussi")

    # ==========================
    # MESSAGE
    # ==========================

    text = "Test SMPP KashPaw"

    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(text)

    print(f"\nNombre de parties : {len(parts)}")

    for index, part in enumerate(parts, start=1):

        print(f"\nEnvoi partie {index}...")

        pdu = client.send_message(

            service_type="",

            source_addr_ton=smpplib.consts.SMPP_TON_INTL,
            source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            source_addr=SOURCE_ADDR,

            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr=DESTINATION,

            esm_class=msg_type_flag,
            protocol_id=0,
            priority_flag=0,

            registered_delivery=True,

            replace_if_present_flag=0,

            data_coding=encoding_flag,

            sm_default_msg_id=0,

            short_message=part
        )

        print("SMS accepté")
        print("Sequence Number :", pdu.sequence)

    print("\nAttente de 2 secondes...")
    client.read_once()

    print("\nDéconnexion...")

    client.unbind()
    client.disconnect()

    print("\n✅ Test terminé avec succès")

except Exception:

    print("\n")
    print("=" * 60)
    print("ERREUR")
    print("=" * 60)

    traceback.print_exc()

    try:
        client.unbind()
    except:
        pass

    try:
        client.disconnect()
    except:
        pass