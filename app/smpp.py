import smpplib.client
import smpplib.consts
import smpplib.gsm

from app.config import Config
from app.logger import logger

class SmppGateway:
    
    def __init__(self):

        self.client = None

        self.connected = False

    def connect(self):
        
        if self.connected:

            return

        logger.info("Connexion au serveur SMPP...")

        self.client = smpplib.client.Client(

            Config.SMPP_HOST,

            Config.SMPP_PORT

        )

        self.client.connect()

        logger.info("Connexion TCP OK")

        self.client.bind_transceiver(

            system_id=Config.SMPP_SYSTEM_ID,

            password=Config.SMPP_PASSWORD

        )

        logger.info("Bind SMPP réussi")

        self.connected = True

    def disconnect(self):
    
        if not self.connected:

            return

        try:

            self.client.unbind()

        except Exception:

            pass

        try:

            self.client.disconnect()

        except Exception:

            pass

        logger.info("Déconnexion SMPP")

        self.connected = False

    def __del__(self):
    
        self.disconnect()

    def send_sms(

        self,

        to: str,

        message: str,

        sender: str = "KashPaw"

    ): 
        if not self.connected:

            self.connect()
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message)

            logger.info( f"Nombre de parties : {len(parts)}")

            sequence = None

            for part in parts:

                try:

                    pdu = self.client.send_message(

                        source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,

                        source_addr_npi=smpplib.consts.SMPP_NPI_UNK,

                        source_addr=sender,

                        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,

                        dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,

                        destination_addr=to,

                        short_message=part,

                        data_coding=encoding_flag,

                        esm_class=msg_type_flag,

                        registered_delivery=False

                    )

                    sequence = pdu.sequence

                    logger.info(

                        f"SMS envoyé : Sequence={sequence}"

                    )

                except Exception as e:

                    logger.error(str(e))

                    raise

            return sequence