from factor import *
from util import compute_elimination_order
class BayesianNetwork:
    """Represents a Bayesian network by its factors, i.e. the conditional probability tables (CPTs).

    Parameters
    ----------
    factors : list[factor.Factor]
        The factors of the Bayesian network
    domains : dict[str, list[str]]
        A dictionary mapping each variable to its possible values
    """

    def __init__(self, factors, domains):
        self.factors = factors
        self.domains = domains
        self.variables = set()
        for factor in self.factors:
            self.variables = self.variables | set(factor.variables)

    def __str__(self):
        return "\n\n".join([str(factor) for factor in self.factors])


def eliminate(bnet, variable):
    """Eliminates a variable from the Bayesian network.

    By "eliminate", we mean that the factors containing the variable are multiplied,
    and then the variable is marginalized (summed) out of the resulting factor.

    Parameters
    ----------
    variable : str
        the variable to eliminate from the Bayesian network

    Returns
    -------
    BayesianNetwork
        a new BayesianNetwork, equivalent to the current Bayesian network, after
        eliminating the specified variable
    """
    relevant_facs = list()
    excluded_facs = list()
    new_domain = dict()
    for factor in bnet.factors:
        if variable in factor.variables:
            relevant_facs.append(factor)
        else:
            excluded_facs.append(factor) #excluding factors without the variable we're looking for

    if not relevant_facs: #in case the network doesnt have any factors with the given variable
        return bnet
    
    multiplied_fac = multiply_factors(relevant_facs, bnet.domains)
    marginalized_fac = marginalize(multiplied_fac, variable)
    new_facs = excluded_facs + [marginalized_fac]
    new_domain = {k: val for k, val in bnet.domains.items() if k != variable}
    new_bnet = BayesianNetwork(new_facs, new_domain)

    return new_bnet 



def compute_marginal(bnet, vars):
    """Computes the marginal probability over the specified variables.

    This method uses variable elimination to compute the marginal distribution.

    Parameters
    ----------
    vars : set[str]
        the variables that we want to compute the marginal over
    """
    #COPIED FROM HANDOUT
    elim_order, _ = compute_elimination_order(bnet)
    revised_elim_order = [var for var in elim_order if var not in vars]
    for var in revised_elim_order:
        bnet = eliminate(bnet, var)
    return multiply_factors(bnet.factors, bnet.domains)
    
    
def compute_conditional(bnet, event, evidence):
    """Computes the conditional probability of an event given the evidence event."""
    # TODO: Implement this for Question Five.
