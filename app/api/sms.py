from fastapi import APIRouter, Depends, HTTPException

from app.auth import verify_token
from app.models import SmsRequest, SmsResponse
from app.services.sms_service import SmsService
from app.logger import logger

router = APIRouter()

sms = SmsService()


@router.post(
    "/send",
    response_model=SmsResponse,
    summary="Envoyer un SMS",
    description="Envoie un SMS via le serveur SMPP Digicel."
)
def send_sms(
    request: SmsRequest,
    token: str = Depends(verify_token)
):
    try:

        logger.info("=" * 60)
        logger.info("Nouvelle requête SMS")
        logger.info(f"Destination : {request.to}")
        logger.info(f"Sender      : {request.sender}")
        logger.info(f"Message     : {request.message}")

        sequence = sms.send(
            to=request.to,
            message=request.message,
            sender=request.sender
        )

        logger.info(f"SMS accepté - Sequence : {sequence}")

        return SmsResponse(
            success=True,
            message="SMS accepté par le serveur SMPP",
            sequence=sequence
        )

    except Exception as e:

        logger.exception("Erreur lors de l'envoi du SMS")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )