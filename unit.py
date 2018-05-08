

class Unit:
    def __init__(self, id,priority, duedate, m, l, origin, destination):
        self.id = id
        self.m = int(m)
        self.l = int(l)
        self.priority = int(priority)
        self.duedate = duedate
        self.origin = int(origin)
        self.destination = int(destination)

    def getPriority(self):
        return self.priority

    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getDueDate(self):
        return self.duedate

    def getMass(self):
        return self.m

    def getLength(self):
        return self.l

    def getNumber(self):
        return 1

    def __str__(self):
        return "Order " + str(self.id) + " with priority "+str(self.getPriority()) + " origin = " + str(self.getOrigin()) + \
               " destination = " + str(self.getDestination()) + " duedate " + str(self.getDueDate())






class Order:
    def __init__(self):
        self.units = []

    def getPriority(self):
        return self.units[0].priority

    def getOrigin(self):
        return self.units[0].origin

    def getDestination(self):
        return self.units[0].destination

    def getDueDate(self):
        return self.units[0].duedate

    def getMass(self):
        return self.units[0].m*len(self.units)

    def getLength(self):
        return self.units[0].l*len(self.units)

    def getNumber(self):
        return len(self.units)

    def addUnit(self, unit):
        self.units.append(unit)

    def __str__(self):
        return "Order with priority "+str(self.getPriority()) + " origin = " + str(self.getOrigin()) + \
               " destination = " + str(self.getDestination()) + " duedate " + str(self.getDueDate())

