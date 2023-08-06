import inspect
import os.path

class Locator():
    def __init__(self,filename=""):
        self.filename = filename
    
    def getlocation(self):
        dirname = os.path.dirname(inspect.getframeinfo(inspect.currentframe().f_back)[0])
        return dirname

    def getfilelocation(self,filename=None):
        if(filename):
            self.filename = filename
        dirname = os.path.dirname(inspect.getframeinfo(inspect.currentframe().f_back)[0])
        return os.path.join(dirname,self.filename)


def test():
    A = Locator("TEST.txt")
    print(A.getfilelocation())

