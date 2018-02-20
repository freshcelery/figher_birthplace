class Fighter():
    def __init__(self, name, location, age, height, weight, weight_class, reach, record):
        self.name = name
        self.location = location
        self.age = int(age)
        self.height = height
        self.weight = weight
        self.weight_class = weight_class
        self.reach = reach
        self.record = record
        self.lat = 0
        self.long = 0
    
    def __str__(self):
        return 'Name: %s, Birthplace: %s, age: %s, height: %s, weight: %s, weight class: %s, reach: %s, record: %s' % (self.name, self.location, self.age, self.height, self.weight, self.weight_class, self.reach, self.record)
