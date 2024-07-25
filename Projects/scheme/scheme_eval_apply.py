import sys
from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
        
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        operator3 = scheme_eval(first, env)
        operands3 = rest.map(lambda operand3: scheme_eval(operand3,env))
        result3 = scheme_apply(operator3,operands3,env)
        return result3
        # return scheme_apply(scheme_eval(first,env) , rest.map(lambda operand :  scheme_eval(operand, env)), env)

        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)

    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        py_args = [] #new list
        while args is not nil: 
            py_args.append(args.first)
            args = args.rest
        if procedure.need_env:
            py_args.append(env)  
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            return procedure.py_func(*py_args)
        
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        child_frame = procedure.env.make_child_frame(procedure.formals,args)
        return eval_all(procedure.body, child_frame)

        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11


        MU_frame = env.make_child_frame(procedure.formals, args)
        return scheme_eval(procedure.body, MU_frame)

        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions is nil:
        return None
    
    else:
        while expressions.rest != nil:
            scheme_eval(expressions.first, env)
            expressions = expressions.rest
        return scheme_eval(expressions.first, env)

    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail = False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        
        # BEGIN PROBLEM EC
        sys.setrecursionlimit(1000000)  #increased limit larger than 501501 

        while True:
            result = unoptimized_scheme_eval(expr, env)

            if isinstance(result, Unevaluated):
                expr, env = result.expr, result.env
            else:
                return result
            
    return optimized_eval

#     # END PROBLEM EC


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)