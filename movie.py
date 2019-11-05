class Movie:
    
    def __init__(self, title=None, original_title=None, duration=None, rating=None, release_date=None):
        self.title = title
        self.duration = duration
        self.original_title = original_title
        self.rating = rating
        self.release_date = release_date
        
        self.actors = []
        self.is3d = None
        self.production_budget = None
        self.marketing_budget = None

    def total_budget(self):
        if (self.production_budget == None) or (self.marketing_budget == None):
            return None

        return self.production_budget + self.marketing_budget

    def __str__(self):
        strings = []
        if hasattr(self, 'id'):
            strings.append('id: ' + str(self.id))
        strings.append('title: ' + str(self.title))
        strings.append('original title: ' + str(self.original_title))
        strings.append('duration: ' + str(self.duration))
        strings.append('rating: ' + str(self.rating))
        strings.append('release date: ' + str(self.release_date))
        return ', '.join(strings)
