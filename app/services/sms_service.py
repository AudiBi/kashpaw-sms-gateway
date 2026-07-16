from typing import Optional

from app.logger import logger
from app.services.smpp_gateway import SmppGateway


class SmsService:
    """
    Service d'envoi des SMS.
    """

    _gateway = SmppGateway()

    def __init__(self):

        self.gateway = SmsService._gateway

    def send(
        self,
        to: str,
        message: str,
        sender: Optional[str] = None,
    ) -> int:

        if not to:
            raise ValueError("Le numéro de destination est obligatoire.")

        if not message:
            raise ValueError("Le message est obligatoire.")

        logger.info("=" * 60)
        logger.info("SmsService")
        logger.info(f"Destination : {to}")
        logger.info(f"Sender      : {sender}")
        logger.info(f"Longueur    : {len(message)} caractères")

        try:

            sequence = self.gateway.send_sms(
                to=to,
                message=message,
                sender=sender,
            )

            logger.info(
                f"SMS envoyé avec succès. Sequence={sequence}"
            )

            return sequence

        except Exception:

            logger.exception("Erreur dans SmsService")

            raise