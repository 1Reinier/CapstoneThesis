import random

class Statistics(object):
    """
    Container for statistical and probabilistic functions.
    """
    def __init__(self):
        pass

    @staticmethod
    def inverse_cdf_pareto(scale, shape, probability):
        """
        Returns the inverse cdf of a Pareto distribution for a given probability, with a scale and a shape parameter.
        The shape parameter is usually called 'alpha' elsewhere.
        """
        return scale / ((1.0 - probability)**(1.0 / shape))

    @staticmethod
    def generate_pareto_number(scale, shape):
        """
        Generates a random number from Pareto distribution with specifies shape and scale parameters.
        """
        probability = random.random()
        return Statistics.inverse_cdf_pareto(scale, shape, probability)

    @staticmethod
    def generate_lognormal_number(mean, standard_deviation):
        """
        Provides an interface to Python's lognormalvariate function.
        """
        return random.lognormvariate(mean, standard_deviation)
