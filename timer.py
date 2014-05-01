class TimeStepper(object):
    """
    Controls time.
    """
    def __init__(self, timestep):
        self.time = 0
        self.step = timestep

    def increment(self):
        '''
        Will increase time by one time step.
        '''
        self.time += self.step

    def _decrement(self):
        '''
        Will decrease time by one time step.
        Not to be used in regular simulation.
        '''
        self.time -= self.step
