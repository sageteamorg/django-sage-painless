class TimingService:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def calculate_execute_time(self, start, end):
        """calculate time taken"""
        return (end - start) * 1000.0
