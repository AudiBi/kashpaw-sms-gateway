import smpplib.client
import smpplib.consts

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
    source_addr_npi=smpplib.consts.SMPP_NPI_UNKNOWN,
    source_addr="KashPaw",
    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
    destination_addr="509XXXXXXXX",
    short_message="Test SMPP"
)

print(pdu)

client.unbind()
client.disconnect()