class Statistics(object):
    """
    Container for statistical and probabilistic functions.
    """
    def __init__(self):
        pass

    def inverse_cdf_pareto(self, scale, shape, probability):
        return scale /((1 - probability)**(1/shape))

    def inverse_cdf_lognormal(self):
        pass
