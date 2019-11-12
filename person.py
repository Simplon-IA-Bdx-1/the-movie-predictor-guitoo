class Person:
    
    def __init__(self, firstname=None, lastname=None, id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.id = id

    def __str__(self):
        strings = []
        strings.append('id: ' + str(self.id))
        strings.append('firstname: ' + str(self.firstname))
        strings.append('lastname: ' + str(self.lastname))
        return ', '.join(strings)
