class dicttoobj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [dicttoobj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, dicttoobj(b) if isinstance(b, dict) else b)


    def jdefault(self):
        return self.__dict__
