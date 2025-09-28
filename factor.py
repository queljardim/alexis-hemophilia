import itertools

class Factor:
    def __init__(self, variables, values):
        self.variables = variables
        self.values = values

    def __getitem__(self, event):
        key = []
        for var in self.variables:
            if var not in event:
                raise KeyError(f"Variable {var} not found in given event.")
            key.append(event[var])
        if tuple(key) in self.values:
            return self.values[tuple(key)]
        else:
            raise KeyError(f"No value assigned to event {event}.")

    def __str__(self):
        result = f"{self.variables}:"
        for event, value in self.values.items():
            result += f"\n  {event}: {value}"
        return result

    __repr__ = __str__


def events(vars, domains):
    all_values = []
    events = []
    all_values += [domains[var] for var in vars] #list of lists
    for combo in itertools.product(*all_values): #tuples like ("P", "yes")
        events.append(dict(zip(vars,combo)))
    return events

def marginalize(factor, variable):
    new_values = dict()
    new_variables = [v for v in factor.variables if v != variable] #all vars but excluded
    
    for combo, val in factor.values.items(): #pair of variables + likelihood 
        combo_dict = dict(zip(factor.variables, combo)) #zip vars with combos
        combo_dict.pop(variable) #take out unwanted var
        new_key = tuple(combo_dict[v] for v in new_variables) #make new key with variable
        new_values[new_key] = new_values.get(new_key, 0) + val #add likelihoods for the variables
    return Factor(new_variables, new_values)

def multiply_factors(factors, domains):
    new_values = dict() #probabilities for assign: ("yes", "u", etc): float
    all_vars = [v for v in domains.keys() if any(v in f.variables for f in factors)] #preserve order in domains
    joint_events = events(all_vars, domains) #all possible ass in all_vars
    for event in joint_events:
        product_val = 1.0 #neutral
        for factor in factors:
            sub = {var: event[var] for var in factor.variables}
            factor_val = factor[sub] #look up probability using dictionary {VAR:X, VAR:Y}
            product_val *= factor_val
        new_key = tuple(event[var] for var in all_vars) #same order as all vars
        new_values[new_key] = product_val
    return Factor(all_vars, new_values)


def create_goat_cpt():
    vars = ['C', 'G']
    probs = {('1', '2'): 0.5, ('1', '3',): 0.5,
             ('2', '2'): 0, ('2', '3',): 1,
             ('3', '2'): 1, ('3', '3',): 0}
    return Factor(vars, probs)


def create_finalchoice_cpt():
    vars = ['G', 'F']
    probs = {('2', '1'): 0, ('2', '2'): 0, ('2', '3',): 1,
             ('3', '1'): 0, ('3', '2'): 1, ('3', '3',): 0}
    return Factor(vars, probs)
