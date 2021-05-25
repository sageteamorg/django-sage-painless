import secrets

from datetime import (
    datetime,
    date
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(
        instance.user.username,
        filename
    )


def date_directory_path(instance, filename):
    today = date.today()
    return f'{today.year}/{today.month}/{today.day}/{filename}'


def date_directory_path(instance, filename):
    today = date.today()
    return f'{secrets.token_hex(7)}/{today.year}-{today.month}-{today.day}/{filename}'


def image_upload_to(instance, filename):
    return '{app_name}/{username}/images/{date}/{filename}'.format(
        app_name=instance.__class__.__name__.lower(),
        username=instance.user.username,
        filename=filename,
        date=datetime.today().strftime('%Y-%m-%d')
    )
