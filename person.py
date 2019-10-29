class Person:
    
    def __init__(self, firstname=None, lastname=None):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        strings = []
        strings.append('id: ' + str(self.id))
        strings.append('firstname: ' + str(self.firstname))
        strings.append('lastname: ' + str(self.lastname))
        return ', '.join(strings)
