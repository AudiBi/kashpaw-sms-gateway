import smpplib.client
import smpplib.consts

HOST = "172.20.222.38"
PORT = 5020

SYSTEM_ID = "KASHPAW"
PASSWORD = "K4$hP4w"

# Si vos variables sont des strings
source_addr_str = "KashPaw"
destination_addr_str = "50948524055"
message_str = "Test SMPP"

# Convertir en bytes
source_addr = source_addr_str.encode('utf-8')
destination_addr = destination_addr_str.encode('utf-8')
short_message = message_str.encode('utf-8')

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
    source_addr=source_addr,  # bytes
    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
    destination_addr=destination_addr,  # bytes
    short_message=short_message  # bytes
)

print(pdu)

client.unbind()
client.disconnect()