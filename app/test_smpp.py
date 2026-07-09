from app.services.sms_service import SmsService

sms = SmsService()

sequence = sms.send(

    to="50948524055",

    message="Test SMS Gateway KashPaw",

    sender="KashPaw"

)

print(sequence)