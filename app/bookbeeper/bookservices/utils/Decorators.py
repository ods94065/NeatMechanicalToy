__author__ = 'keaj'
class Singleton():
    def __init__(self,decoratedclass):
        self._decoratedclass=decoratedclass
    def GetInstance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decoratedclass()
            return self._instance
    def __Call__(self):
        raise TypeError("Singletons can't be instantiated at will. Call GetInstance to get the singleton.")
    def __instancecheck__(self,inst):
        return isinstance(inst,self._decoratedclass)