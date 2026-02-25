class Constructor:
    def __init__(self, name, cost, points):
        self.name = name
        self.cost = cost
        self.points = points
        self.drivers = []  # List to hold Driver objects

    def __repr__(self):
        return f"Constructor({self.name})"

class Driver:
    def __init__(self, name, cost, points, constructor: Constructor):
        self.name = name
        self.cost = cost
        self.points = points
        self.constructor = constructor
        # Link the driver back to the constructor's list
        constructor.drivers.append(self)

    def __repr__(self):
        return f"Driver({self.name}, Team: {self.constructor.name})"