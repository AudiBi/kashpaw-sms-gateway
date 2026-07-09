from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.auth import verify_token

from app.models import SmsRequest
from app.models import SmsResponse

from app.services.sms_service import SmsService

router = APIRouter()

sms = SmsService()


@router.post(
    "/send",
    response_model=SmsResponse
)
def send_sms(

    request: SmsRequest,

    token: str = Depends(verify_token)

):

    try:

        sequence = sms.send(

            request.to,

            request.message,

            request.sender

        )

        return SmsResponse(

            success=True,

            message="SMS envoyé",

            sequence=sequence

        )

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )