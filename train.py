

class Stop:
    def __init__(self, station, arrTime, endTime):
        self.station = station
        self.arrTime = arrTime
        self.endTime = endTime

class Activity:

    def __init__(self, type, station, n, start, end):
        self.type = type
        self.station = station
        self.n = n
        self.orders = []
        self.start = start
        self.end = end

    def addOrder(self, order):
        self.orders.append(order)

    def Orders(self):

        res = ""
        for x in self.orders:
            res += str(x) + " ; "

        return res



class Train:
    def __init__(self, timetable, max_m, max_l, id):

        self.id = id
        self.timetable = timetable
        self.max_mass = max_m
        self.max_length = max_l
        self.activities = []
        self.current_mass = 0
        self.current_length = 0
        for x in timetable:
            self.activities.append(Activity("waiting1", x.station, 0, x.arrTime, x.arrTime + (x.endTime-x.arrTime)/2))
            self.activities.append(Activity("waiting2", x.station, 0, x.arrTime + (x.endTime-x.arrTime)/2, x.endTime))

    def addActivity(self, order, n):
        for x in self.activities:
            if int(x.station) == int(order.getOrigin()) and (x.type == "waiting2" or x.type == "pickup"):
                self.activities[self.activities.index(x)].type = "pickup"
                self.activities[self.activities.index(x)].addOrder(order)
                self.current_mass += order.getMass()/order.getNumber()*n
                self.current_length += order.getLength()/order.getNumber()*n
            if int(x.station) == int(order.getDestination()) and (x.type == "waiting1" or x.type == "delivery"):
                self.activities[self.activities.index(x)].type = "delivery"
                self.activities[self.activities.index(x)].addOrder(order)

    def getTime(self, station):
        for t in self.timetable:
            if int(t.station) == int(station):
                return t.arrTime + (t.endTime-t.arrTime)/2


    def getStartTime(self, station):
        for t in self.timetable:
            if int(t.station) == int(station):
                return t.arrTime

    def print(self):
        print("train")
        for activity in self.activities:
            print(activity.type, " ",activity.station," [", str(activity.start),'-',str(activity.end),'] ', activity.Orders())




