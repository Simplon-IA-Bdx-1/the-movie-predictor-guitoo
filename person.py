class Person:
    
    def __init__(self, name=None,  imdb_id=None):
        self.name = name
        self.imdb_id = imdb_id
#       self.id = id

    def __str__(self):
        strings = []
        strings.append('id: ' + str(self.imdb_id))
        strings.append('name: ' + str(self.name))
        return ', '.join(strings)
