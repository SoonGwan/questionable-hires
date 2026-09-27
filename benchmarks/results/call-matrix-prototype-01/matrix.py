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


def observe(call, cases, *, examples=3):
    """cases: (input, {'return': value} | {'raises': ExceptionClass}).

    Callback gets a disposable deepcopy. Exceptions are recorded by exact class;
    exception messages are not part of this prototype's contract. Return values
    are compared with Python equality. No manually predicted mismatch count.
    Nonprimitive inputs/results, invalid expectations or report failures abort;
    they are not silently converted into passes or dropped observations.
    """
    if type(cases) is not list or not 1 <= len(cases) <= 256:
        raise ValueError('provide 1..256 explicit cases')
    if type(examples) is not int or not 1 <= examples <= 8:
        raise ValueError('provide 1..8 examples')
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
    result=dict(cases=len(cases),matches=0,mismatches=0,input_mutations=0,examples=[],complete=True)
    for number,(case,expected,encoded_input,encoded_expected) in enumerate(prepared):
        argument=copy.deepcopy(case);before=copy.deepcopy(argument)
        try:
            actual=call(argument)
        except Exception as error:
            encoded_actual={'raises':type(error).__module__+'.'+type(error).__qualname__}
            match='raises' in expected and type(error) is expected['raises']
        else:
            encoded_actual={'return':_value(actual)}
            match='return' in expected and actual==expected['return']
        mutation=argument!=before
        result['input_mutations']+=bool(mutation)
        result['matches' if match and not mutation else 'mismatches']+=1
        if (not match or mutation) and len(result['examples'])<examples:
            result['examples'].append(dict(case=number,input=encoded_input,expected=encoded_expected,actual=encoded_actual,input_mutated=mutation))
    result['omitted_mismatch_examples']=result['mismatches']-len(result['examples'])
    return result
