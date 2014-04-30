class TimeStepper(object):
    """
    Controls time.
    """
    def __init__(self, timestep):
        self.time = 0
        self.step = timestep

    def increment(self):
        self.time += self.step

    def decrement(self):
        self.time -= self.step
