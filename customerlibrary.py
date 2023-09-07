class CustomerLibs():

    def __init__(self, id=0 , username=None , password=None):
        self.id=id
        self.username=username
        self.password=password

    def getId(self):
        return self.id
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setId(self , id):
        return self.id
    
    def setUsername(self , username):
        return self.username
    
    def setPassword(self , password):
        return self.password
    
    def __str__(self):
        return ('{}.{},{}'.format(self.id, self.username, self.password))