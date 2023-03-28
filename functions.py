import json

def ot(my_list: list, soz: str, lotin=False):
    if lotin:
        for i in my_list:
            if soz == i["lotincha-bosh-birlik"]:
                return i
        return -1
    else:
        for i in my_list:
            for j in i["ozbekcha-bosh-birlik"]:
                if soz == j:
                    return i
        return -1
    
def f(map_: dict):
    a = map_["lotincha-bosh-birlik"]
    b = map_["lotincha-qaratqich-birlik-qoshimcha"]
    c = map_["rod"]
    return "a) Lotincha bosh kelishik birlikda:\n{}\n\nb) Lotincha qaratqich kelishigi birlikda qo'shimchasi: {}\n\nc) Rodi: {}".format(a, b, c)
    
def tutuq_belgisi(s: str):
    res = ""
    for i in s:
        if i == "\u02bc" or i == "\u02bb":
            res += "'"
        else:
            res += i
    return res

def g(s: str):
    x = 0
    y = 0
    a = 0
    b = 0
    for i, e in enumerate(s):
        if e == "(":
            x = i
        elif e == ")":
            y = i
        elif e == "[":
            a = i
        elif e == "]":
            b = i
        else:
            pass
    n = s[x+1:y].split(" ") 
    m = s[a+1:b].split(" ")
    di = {}
    
    di["lotincha-bosh-birlik"] = n[0]
    di["lotincha-qaratqich-birlik-qoshimcha"] = n[1]
    di["ozbekcha-bosh-birlik"] = m
    di["rod"] = n[2]
    return di
    
