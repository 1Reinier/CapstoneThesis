class TimeStepper(object):
    """
    Controls time.
    """
    def __init__(self, timestep):
        """
        :type timestep: int
        """
        self.time = 0
        assert (timestep > 0), 'Only positive numbers allowed'
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
