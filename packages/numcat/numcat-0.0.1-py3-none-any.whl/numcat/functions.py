def concat(a: float, b: float) -> float:
    """Concatenates two numbers together

    Parameters
    ----------
    a : float
        The first number in the concatenation
    b : float
        The second number in the concatenation

    Returns
    -------
    c : float
        The concatenated number
    """
    a,b = float(a),float(b)
    if a == -0.0:
        a = 0.0
    if b == -0.0:
        b = 0.0
    if str(a)[0] == '-' or str(b)[0] == '-':
        if str(a)[0] == '-' and str(b)[0] == '-':
            a1, a2 = str(a)[1::].split('.')
            b1, b2 = str(b)[1::].split('.')
            return float(a1+b1+'.'+a2+b2)
        else:
            if str(a)[0] == '-':
                a1, a2 = str(a)[1::].split('.')
                b1, b2 = str(b).split('.')
                return -float(a1+b1+'.'+a2+b2)   
            elif str(b)[0] == '-':
                a1, a2 = str(a).split('.')
                b1, b2 = str(b)[1::].split('.')
                return -float(a1+b1+'.'+a2+b2)                          
    else:
        a1, a2 = str(a).split('.')
        b1, b2 = str(b).split('.')
        return float(a1+b1+'.'+a2+b2)
    
def concatZero(a: str, b: str) -> float:
    """Concatenates two numbers together including trailing zeros

    Parameters
    ----------
    a : float
        The first number in the concatenation
    b : float
        The second number in the concatenation

    Returns
    -------
    c : float
        The concatenated number
    """
    if a == "-0.0":
        a = "0.0"
    if b == "-0.0":
        b = "0.0"
    if a[0] == '-' or b[0] == '-':
        if a[0] == '-' and b[0] == '-':
            a1, a2 = a[1::].split('.')
            b1, b2 = b[1::].split('.')
            return float(a1+b1+'.'+a2+b2)
        else:
            if a[0] == '-':
                a1, a2 = a[1::].split('.')
                b1, b2 = b.split('.')
                return -float(a1+b1+'.'+a2+b2)   
            elif b[0] == '-':
                a1, a2 = a.split('.')
                b1, b2 = b[1::].split('.')
                return -float(a1+b1+'.'+a2+b2)                          
    else:
        a1, a2 = a.split('.')
        b1, b2 = b.split('.')
        return float(a1+b1+'.'+a2+b2)
    
def concatArr(l: list[int]) -> float:
    """Concatenates a array of numbers together

    Parameters
    ----------
    l : list[int]
        A list of integers to be concatenated

    Returns
    -------
    c : float
        The concatenated number
    """
    tmp = []
    for i in range(0,len(l),2):
        if i < len(l)-1:
            tmp.append(concat(l[i],l[i+1]))
        else:
            tmp.append(l[i])
    if len(l) > 1:
        return concatArr(tmp)
    else:
        return float(tmp[0])
    
def concatArrZero(l: list[str]) -> float:
    """Concatenates a array of numbers together including trailing zeros

    Parameters
    ----------
    l : list[int]
        A list of integers to be concatenated

    Returns
    -------
    c : float
        The concatenated number
    """
    tmp = []
    for i in range(0,len(l),2):
        if i < len(l)-1:
            tmp.append(concatZero(l[i],l[i+1]))
        else:
            tmp.append(l[i])
    if len(l) > 1:
        return concatArr(tmp)
    else:
        return float(tmp[0])