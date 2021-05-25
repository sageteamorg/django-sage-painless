import secrets
import json
import random
from _datetime import timedelta

from rest_framework import status

from django_celery_beat.models import ClockedSchedule, PeriodicTask

from django.utils.translation import ugettext_lazy as _

from authentication.models import OTP_History
from authentication.tasks import send_otp


class OTP_Token_API:
    def __init__(self, phone_number, scope, *args, **kwargs):
        self.token_existence_message = kwargs.get('token_existence_message', _("Token already is sent. Please use it."))
        self.send_sms_message = kwargs.get('send_sms_message',
                                           _("An sms is sent to your phone number. Please add sent code to text box."))

        self.phone_number = phone_number
        self.scope = scope

    def generate(self, max_size):
        return ''.join(random.sample('123456789', max_size))

    def get_instance(self):
        return OTP_History.objects.filter(phone_number=self.phone_number).filter(is_active=True).filter(
            scope=self.scope).first()

    def __check_token_existence(self):
        otp_obj = OTP_History.objects.filter(phone_number=self.phone_number).filter(is_active=True).filter(
            scope=self.scope)
        return otp_obj.exists()

    def __create(self):
        otp = OTP_History.objects.create(
            phone_number=self.phone_number,
            scope=self.scope,
            token=self.generate(6)
        )
        return otp

    def __schedule(self, otp_obj):
        clocked, created = ClockedSchedule.objects.get_or_create(
            clocked_time=otp_obj.expiration_time,
        )

        PeriodicTask.objects.create(
            clocked=clocked,
            name=f"OTP-{otp_obj.phone_number}-{secrets.token_hex(7)}",
            task='authentication.tasks.otp_expiration',
            kwargs=json.dumps({"otp_pk": otp_obj.pk.__str__()}),
            start_time=otp_obj.send_time,
            expires=otp_obj.expiration_time + timedelta(seconds=10),
            one_off=True
        )

    def __send_sms(self, otp_obj=None):
        if otp_obj.token:
            # schedule sending sms
            # clocked = ClockedSchedule.objects.create(
            #     clocked_time=otp_obj.send_time + timedelta(seconds=1)
            # )
            # PeriodicTask.objects.create(
            #     name=f'SEND-OTP-{self.phone_number}-{otp_obj.token}-{secrets.token_urlsafe(6)}',
            #     task='authentication.tasks.send_otp',
            #     clocked=clocked,
            #     kwargs=json.dumps({'phone_number': self.phone_number, 'token': otp_obj.token}),
            #     one_off=True,
            #     expire_seconds=10
            # )
            task = send_otp.apply_async(kwargs={
                'phone_number': otp_obj.phone_number,
                'token': otp_obj.token
            }, queue='otp')
            # message, send = iran_otp.send_token(self.phone_number, token)
            message, send = task.state, True  # TODO: change message and send
        else:
            # schedule sending sms
            # clocked = ClockedSchedule.objects.create(
            #     clocked_time=datetime.now()
            # )
            # PeriodicTask.objects.create(
            #     name=f'SEND-OTP-{self.phone_number}-{otp_obj.token}-{secrets.token_urlsafe(6)}',
            #     task='authentication.tasks.send_otp',
            #     clocked=clocked,
            #     kwargs=json.dumps({'phone_number': self.phone_number, 'token': self.generate(6)}),
            #     one_off=True,
            #     expire_seconds=1
            # )
            task = send_otp.apply_async(kwargs={
                'phone_number': otp_obj.phone_number,
                'token': otp_obj.token
            }, queue='otp')
            # message, send = iran_otp.send_token(self.phone_number, self.generate(6))
            message, send = task.state, True

        return message, send

    def send_otp(self, otp_type='iran_otp'):
        message = None
        if otp_type == 'iran_otp':

            if self.__check_token_existence():
                message = self.token_existence_message
                code = status.HTTP_403_FORBIDDEN
            else:
                otp = self.__create()
                message, send = self.__send_sms(otp_obj=otp)
                if send:
                    message = self.send_sms_message
                    code = status.HTTP_201_CREATED
                    self.__schedule(otp)
                else:
                    message = 'Bad Request'
                    code = status.HTTP_400_BAD_REQUEST

        elif otp_type == 'twilio':
            pass

        return message, code

    def verify_otp(self, token):
        otp_obj = OTP_History.objects.filter(phone_number=self.phone_number).filter(is_active=True).filter(
            scope=self.scope)
        if not otp_obj.exists():
            return False

        otp_obj = otp_obj.first()

        if not token == otp_obj.token:
            return False

        return True
