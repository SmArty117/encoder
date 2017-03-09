__author__ = 'Dan'

supported_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def getcodes():
    CodesIn = open("codes.in", "r")
    codes = []
    code = CodesIn.readline()
    strlen = len(code)
    while code != '\n':

        codes.append(code[0:-1])
        code = CodesIn.readline()
        if len(code) != strlen:
            break

    CodesIn.close()
    return codes

codes = getcodes()

def toint(c):
    """
    :rtype : int
    """
    a = ord('a')
    z = ord('z')
    A = ord('A')
    Z = ord('Z')
    if c in supported_chars:
        c = ord(c)
        if A <= c <= Z:
            return c-A
        if a <= c <= z:
            return c-a
        if ord('0') <= c <= ord('9'):
            return c-ord('0') + 26
    else: return -1


def tochar(c):
    """
    :rtype : str
    """
    if c>=0 and c<=25:
        return chr(c+ord('a'))
    if c>=26 and c<=35:
        return chr(c-26+ord('0'))
    else:
        return -1


def advance(nrs, maxnr):
    nrs[0] += 1
    for i in xrange(len(nrs)):
        if nrs[i] >= maxnr:
            nrs[i] -= maxnr
            nrs[i+1] += 1
    assert isinstance(nrs, list)
    return nrs


def encode(S, nrs, codes):

    if codes == "CORRUPT CODES":
        return codes

    ans = ""
    strlen = len(codes[0])

    for i in xrange(len(nrs)):
        nrs[i] = nrs[i]%strlen

    try:
        for c in S:
            cc = c
            for i in xrange(len(codes)):
                code = codes[i]
                offset = nrs[i]
                numc = toint(cc)
                if numc != -1:
                    cc = code[(numc+offset)%strlen]
            ans += cc
            nrs = advance(nrs, strlen)
        return ans

    except:
        return "INVALID INPUT\n"

def DecrGen(start, stop = 0, step = 1):
    i = start - step
    while i >= stop:
        yield i
        i -= step


def decode(S, nrs, codes):

    if codes == "CORRUPT CODES":
        return codes

    ans = ""
    strlen = len(codes[0])

    for i in xrange(len(nrs)):
        nrs[i] = nrs[i]%strlen

    try:
        for c in S:
            cc = c
            for i in DecrGen(len(codes)):
                code = codes[i]
                offset = nrs[i]
                posc = code.find(cc)
                if posc != -1:
                    posc -= offset
                    if posc < 0:
                        posc += strlen
                    cc = tochar(posc)
            ans += cc
            nrs = advance(nrs, strlen)
        return ans

    except:
        return "INVALID INPUT\n"
