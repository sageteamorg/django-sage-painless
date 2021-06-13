class Signal:
    def __init__(self):
        self.model_b = None
        self.model_a = None
        self.method = None
        self.field = None

    def set_signal(self, method, sender, dest, field):
        self.method = method
        self.model_a = sender
        self.model_b = dest
        self.field = field
