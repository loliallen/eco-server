

def dict_to_update(dict: object) -> object:
    dd = {}
    for k in dict.keys():
        dd['set__'+k] = dict[k]
    return dd