import sympy


def solve_ctmc(transitions, state_list=None):
    '''
    Solves a Continous Time Markov Chain

    Parameters:
        transitions - dict representing a CTMC
        state_list - ordered list of the states

    Returns:
        dict mapping state names to steady state probabilities

    The format of the CTMC is a dict mapping a tuple of two strings
    ('from_state', 'to_state') to a rate. This rate can be either a
    number or a Sympy expression.
    '''

    if state_list is None:
        state_set = set(t[i] for i in (0, 1) for t in transitions)
        state_list = list(state_set)
    n_states = len(state_list)
    Q = sympy.zeros(n_states, n_states)
    ix = {s: i for i, s in enumerate(state_list)}
    for (pred, succ), rate in transitions.items():
        Q[ix[pred], ix[succ]] = rate
    for i in range(Q.rows):
        Q[i, i] = -sum(Q.row(i))
    Q.col_del(n_states-1)
    Q = Q.T
    Q = Q.row_insert(len(Q), sympy.Matrix([[1]*n_states]))
    b = sympy.Matrix([[0]]*(n_states-1) + [[1]])
    solution_set = sympy.linsolve((Q, b), sympy.symbols(state_list))
    actual_sol = list(solution_set)[0]
    return {state: actual_sol[ix[state]] for state in state_list}
