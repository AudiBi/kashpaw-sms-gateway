import logging
from typing import Optional

import smpplib.client
import smpplib.consts
import smpplib.gsm

from app.config import Config
from app.logger import logger

# Active les logs de la librairie smpplib
logging.getLogger("smpplib").setLevel(logging.DEBUG)


class SmppGateway:
    """
    Gestionnaire de connexion SMPP.
    """

    def __init__(self):
        self.client: Optional[smpplib.client.Client] = None
        self.connected = False

    def connect(self) -> None:
        """
        Connexion au serveur SMPP.
        """

        if self.connected and self.client:
            logger.info("Connexion SMPP déjà active.")
            return

        logger.info("=" * 60)
        logger.info("Connexion au serveur SMPP")
        logger.info("=" * 60)

        try:
            self.client = smpplib.client.Client(
                Config.SMPP_HOST,
                Config.SMPP_PORT,
            )

            self.client.connect()

            logger.info("Connexion TCP réussie.")

            self.client.bind_transceiver(
                system_id=Config.SMPP_SYSTEM_ID,
                password=Config.SMPP_PASSWORD,
            )

            self.connected = True

            logger.info("Bind SMPP réussi.")

        except Exception as e:

            self.connected = False

            logger.exception("Erreur pendant la connexion SMPP")

            raise RuntimeError(
                f"Impossible de se connecter au serveur SMPP : {e}"
            )

    def disconnect(self) -> None:
        """
        Déconnexion propre.
        """

        if not self.client:
            return

        try:
            logger.info("Unbind SMPP...")
            self.client.unbind()
        except Exception:
            pass

        try:
            logger.info("Déconnexion TCP...")
            self.client.disconnect()
        except Exception:
            pass

        self.connected = False
        self.client = None

        logger.info("Déconnexion terminée.")

    def reconnect(self):
        """
        Reconnexion.
        """

        logger.warning("Reconnexion SMPP...")

        self.disconnect()

        self.connect()

    def send_sms(
        self,
        to: str,
        message: str,
        sender: str = None,
    ):
        """
        Envoi d'un SMS.
        """

        if sender is None:
            sender = Config.SMPP_SOURCE_ADDR

        if not self.connected:
            self.connect()

        logger.info("-" * 60)
        logger.info("Début envoi SMS")
        logger.info(f"Destination : {to}")
        logger.info(f"Sender      : {sender}")
        logger.info(f"Message     : {message}")

        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(
            message
        )

        logger.info(f"Nombre de parties : {len(parts)}")

        sequence = None

        for index, part in enumerate(parts, start=1):

            logger.info(f"Envoi partie {index}/{len(parts)}")

            try:

                pdu = self.client.send_message(

                    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,

                    source_addr_npi=smpplib.consts.SMPP_NPI_UNKNOWN,

                    source_addr=sender,

                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,

                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,

                    destination_addr=to,

                    short_message=part,

                    data_coding=encoding_flag,

                    esm_class=msg_type_flag,

                    registered_delivery=True,

                )

                logger.info("=" * 60)
                logger.info("submit_sm envoyé")
                logger.info("=" * 60)

                logger.info(f"PDU       : {pdu}")

                if hasattr(pdu, "sequence"):
                    sequence = pdu.sequence
                    logger.info(f"Sequence  : {sequence}")

                if hasattr(pdu, "status"):
                    logger.info(f"Status    : {pdu.status}")

                if hasattr(pdu, "message_id"):
                    logger.info(f"MessageID : {pdu.message_id}")

            except Exception as e:

                logger.exception("Erreur submit_sm")

                raise RuntimeError(
                    f"Erreur SMPP : {e}"
                )

        logger.info("SMS soumis au SMSC.")

        return sequence

    def __del__(self):
        self.disconnect()