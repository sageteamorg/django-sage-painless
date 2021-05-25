from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils import timezone
from datetime import timedelta
from django.db import models
from painless.utils.models.validations import PersianPhoneNumberValidator


class OTPHistory(models.Model):
    SCOPES = (
        ('r', 'Register'),
        ('l', 'login'),
        ('p', 'Reset Password'),
    )

    token = models.CharField(
        max_length=6,
        validators=[
            MaxLengthValidator(6),
            MinLengthValidator(6)
        ]
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            PersianPhoneNumberValidator
        ]
    )
    scope = models.CharField(max_length=1, choices=SCOPES)

    send_time = models.DateTimeField()
    expiration_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        """ Unicode representation of OTPHistory. """
        return f'{self.token} - {self.phone_number}'

    def save(self, *args, **kwargs):
        """ Save method for OTPHistory. """
        self.send_time = timezone.now()
        self.expiration_time = self.send_time + timedelta(minutes=2)
        super(OTPHistory, self).save(*args, **kwargs)