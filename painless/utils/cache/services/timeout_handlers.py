import importlib
from datetime import datetime


def get_subscription_timedelta(user):
    """
    calculates user's in progress subscription timedelta
    """
    if user.is_authenticated:
        membership = user.memberships.filter(status='i')
        if not membership.exists():
            return 3600
        membership = membership.first()
        duration = membership.expires_at - datetime.now().date()
        return duration.total_seconds()
    return 60


def get_timeout(user, func):
    module = func.split('.')
    function = module.pop(-1)
    import_string = '.'.join(module)
    module = importlib.import_module(import_string)
    function = getattr(module, function)
    return function(user)
