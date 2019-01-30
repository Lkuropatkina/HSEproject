from DraftParser import parse

def answer(s):
    result = parse(s)
    return ("$" + str(result) + "$", result.compute())
