"""Local prototype: execute explicit callback cases and summarize observations.

Not a sandbox, a source loader, an assertion replacement or an installed skill.
Caller owns source binding, inputs, expected contract and execution deadline.
"""
import copy


def _value(value, depth=0):
    if depth > 4:
        raise ValueError('report value exceeds depth limit')
    if value is None or type(value) in (bool, int, str):
        if type(value) is int and value.bit_length() > 256:
            raise ValueError('report integer too large')
        if type(value) is str and len(value) > 256:
            raise ValueError('report string too long')
        return value
    if type(value) in (list, tuple) and len(value) <= 16:
        return {'type': type(value).__name__, 'items': [_value(v, depth+1) for v in value]}
    if type(value) is dict and len(value) <= 16 and all(type(k) is str and len(k) <= 128 for k in value):
        return {'type':'dict','items':{k:_value(v,depth+1) for k,v in value.items()}}
    raise ValueError('unsupported report value')


def observe(call, cases, *, examples=3, retain=False):
    """cases: (input, {'return': value} | {'raises': ExceptionClass}).

    Callback gets a disposable deepcopy. Exceptions are recorded by exact class;
    exception messages are not part of this prototype's contract. Return values
    are compared with Python equality. No manually predicted mismatch count.
    Invalid inputs/expectations abort before calls. Unsupported actual returns
    yield complete=False with prior observations, attempted/evaluated/unrun
    counts and the encoding error. Check complete before using the summary.
    retain=True adds ordered encoded actual outcomes for evaluated cases, including
    matches; no callback replay. On encoding failure only the graded prefix is
    retained; inspect complete/ungraded/unrun before using it as full evidence.
    BaseException interruptions still propagate; this is not a process supervisor.
    """
    if type(cases) is not list or not 1 <= len(cases) <= 256:
        raise ValueError('provide 1..256 explicit cases')
    if type(examples) is not int or not 1 <= examples <= 8:
        raise ValueError('provide 1..8 examples')
    if type(retain) is not bool:
        raise ValueError('retain must be bool')
    prepared=[]
    for case,expected in cases:
        encoded_input=_value(case)
        if type(expected) is not dict or len(expected)!=1:
            raise ValueError('one return or raises expectation required')
        if 'return' in expected:
            encoded_expected={'return':_value(expected['return'])}
        elif 'raises' in expected and isinstance(expected['raises'],type) and issubclass(expected['raises'],Exception):
            encoded_expected={'raises':expected['raises'].__module__+'.'+expected['raises'].__qualname__}
        else:
            raise ValueError('invalid expectation')
        prepared.append((case,expected,encoded_input,encoded_expected))
    result=dict(version=2,cases=len(cases),calls_attempted=0,cases_evaluated=0,unrun=len(cases),ungraded=0,matches=0,mismatches=0,input_mutations=0,examples=[],complete=True,omitted_mismatch_examples=0)
    if retain:
        result['version']=3
        result['observations']=[]
    for number,(case,expected,encoded_input,encoded_expected) in enumerate(prepared):
        argument=copy.deepcopy(case);before=copy.deepcopy(argument)
        result['calls_attempted']+=1
        result['unrun']-=1
        try:
            actual=call(argument)
        except Exception as error:
            encoded_actual={'raises':type(error).__module__+'.'+type(error).__qualname__}
            match='raises' in expected and type(error) is expected['raises']
        else:
            try:
                encoded_actual={'return':_value(actual)}
            except ValueError as error:
                result.update(complete=False,ungraded=1,error=dict(case=number,stage='return_encoding',type=type(error).__name__,message=str(error)))
                result['input_mutations']+=bool(argument!=before)
                return result
            match='return' in expected and actual==expected['return']
        if retain:
            result['observations'].append(encoded_actual)
        result['cases_evaluated']+=1
        mutation=argument!=before
        result['input_mutations']+=bool(mutation)
        result['matches' if match and not mutation else 'mismatches']+=1
        if (not match or mutation) and len(result['examples'])<examples:
            result['examples'].append(dict(case=number,input=encoded_input,expected=encoded_expected,actual=encoded_actual,input_mutated=mutation))
        result['omitted_mismatch_examples']=result['mismatches']-len(result['examples'])
    return result
