import threading
import time

import smpplib.client
import smpplib.consts
import smpplib.gsm

from app.config import Config
from app.logger import logger


class SmppGateway:

    def __init__(self):

        self.client = None
        self.connected = False
        self.lock = threading.Lock()

    def connect(self):

        with self.lock:

            if self.connected and self.client:
                return

            logger.info("=" * 60)
            logger.info("Connexion au serveur SMPP")
            logger.info("=" * 60)

            try:

                self.client = smpplib.client.Client(
                    Config.SMPP_HOST,
                    Config.SMPP_PORT
                )

                self.client.set_message_received_handler(
                    self.on_message_received
                )

                self.client.connect()

                logger.info("Connexion TCP OK")

                self.client.bind_transceiver(
                    system_id=Config.SMPP_SYSTEM_ID,
                    password=Config.SMPP_PASSWORD
                )

                logger.info("Bind SMPP réussi")

                self.connected = True

            except Exception:

                self.connected = False

                logger.exception("Impossible de se connecter au SMSC")

                raise

    def disconnect(self):

        with self.lock:

            if self.client is None:
                return

            try:
                self.client.unbind()
            except Exception:
                pass

            try:
                self.client.disconnect()
            except Exception:
                pass

            self.client = None
            self.connected = False

            logger.info("Déconnexion SMPP")

    def reconnect(self):

        logger.warning("Reconnexion SMPP...")

        self.disconnect()

        time.sleep(1)

        self.connect()

    def on_message_received(self, pdu, **kwargs):

        logger.info(f"DeliverSM : {pdu}")

    def ensure_connection(self):

        if not self.connected:
            
            self.disconnect()
            self.connect()

            return

        try:

            self.client.read_once()

        except Exception:

            logger.warning("Connexion SMPP perdue.")

            self.reconnect()

    def send_sms(
        self,
        to: str,
        message: str,
        sender: str = None
    ):

        self.ensure_connection()

        if sender is None:
            sender = Config.SMPP_SOURCE_ADDR

        logger.info("=" * 60)
        logger.info("Nouvelle demande d'envoi")
        logger.info(f"Destination : {to}")
        logger.info(f"Sender      : {sender}")

        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(
            message
        )

        logger.info(f"{len(parts)} partie(s)")

        sequence = None

        try:

            for index, part in enumerate(parts, start=1):

                logger.info(
                    f"Envoi partie {index}/{len(parts)}"
                )

                pdu = self.client.send_message(

                    service_type="",

                    source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    source_addr=sender,

                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    destination_addr=to,

                    esm_class=msg_type_flag,

                    protocol_id=0,

                    priority_flag=0,

                    registered_delivery=True,

                    replace_if_present_flag=0,

                    data_coding=encoding_flag,

                    sm_default_msg_id=0,

                    short_message=part

                )

                sequence = pdu.sequence

                logger.info(
                    f"submit_sm OK - Sequence={sequence}"
                )

                self.client.read_once()

            logger.info("SMS envoyé avec succès")

            return sequence

        except Exception:

            logger.exception("Erreur d'envoi")

            self.connected = False

            raise