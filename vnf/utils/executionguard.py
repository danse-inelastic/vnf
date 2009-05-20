

def validate(code, excluded=['import', 'exec', 'eval', 'builtin', 'global']):
    """find out if the code piece has "dangerous" python words that
    could be used to do import. 

    The purpose of this function is to make sure the given piece
    of code would not be able to do import. This way, this
    piece of code can only be executed within a restricted
    environment.

    This can be easily exploited however, as pointed out by Paul Kienzle.
    But I won't tell you how :)
    """
    code = code.lower()
    for word in excluded:
        if code.find(word) != -1: return False
        continue
    return True



def test_validate():
    badcodes = [
        "import os",
        'eval(1)',
        'exec "a=1"',
        ]
    for piece in badcodes:
        assert validate(piece) == False
    return


def test_usage():
    precode = 'from numpy import sin'
    code = 'print sin(1.0)'
    assert validate(code)

    tobeexec = '\n'.join([precode, code])
    exec tobeexec in {}
    return


def test():
    test_validate()
    test_usage()
    return


if __name__ == '__main__': test()
