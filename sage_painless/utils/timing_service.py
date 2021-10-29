"""
django-sage-painless - Timing Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""


class TimingService:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    @classmethod
    def calculate_execute_time(cls, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0
