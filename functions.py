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

