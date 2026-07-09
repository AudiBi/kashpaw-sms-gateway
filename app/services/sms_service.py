from app.smpp import SmppGateway


class SmsService:

    def __init__(self):

        self.gateway = SmppGateway()

    def send(

        self,

        to,

        message,

        sender="KashPaw"

    ):

        return self.gateway.send_sms(

            to,

            message,

            sender

        )