
class Solution:
    cost_by_minute = 1
    cost_by_unassigned = 1000

    def __init__(self, trains, orders):
        self.trains = trains
        self.unassigned_orders = orders


    def calculateCost(self):
        cost = 0

        for train in self.trains:
            for activity in train.activities:
                if 'waiting' not in activity.type:
                    for order in activity.orders:
                        if order.getDueDate() < train.getTime(activity.station):
                            cost += max(0,(train.getTime(activity.station) - order.getDueDate()).seconds/60)*self.cost_by_minute

        cost += self.cost_by_unassigned*len(self.unassigned_orders)

        return cost


    def printSolution(self):
        print("Cost = " + str(self.calculateCost()))
        for train in self.trains:
            print("train " + train.id)
            for activity in train.activities:
                print(activity.type, " ",activity.station," [", str(activity.start),'-',str(activity.end),'] ', activity.Orders())

        if len(self.unassigned_orders) != 0:
            print("Unassigned jobs")
            for job in self.unassigned_orders:
                print(job)
