from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
from solution import Solution
from train import Train, Stop
from unit import Unit,Order
from railgraph import RailGraph

import constraints

class Algorithm:


    def __init__(self, dir):

        self.trains = []
        self.orders = []
        self.bad_jobs = []
        self.hard_constraints = []
        self.soft_constraints = []
        # all_orders = []
        trains_file = open(dir + "/trains",'r')
        order_file = open(dir + "/orders",'r')
        for o in order_file.readlines()[1:]:
            id, priority,origin,destination,duedate,m,l,n,tmp = o.split(";")
            duedateDate = datetime.strptime(duedate, '%d.%m.%y %H:%M')
            # order = Order()
            for i in range(int(n)):
                self.orders.append(Unit(id, priority,duedateDate,m,l,origin,destination))




        lines = trains_file.readlines()[1:]
        i = 0
        while i < len(lines):
            t = lines[i]
            train, station, arrive, departure, tmp = t.split(';')
            id = train
            stops = []
            while id == train:
                arriveTime = datetime.strptime(arrive, '%d.%m.%y %H:%M')
                departureTime = datetime.strptime(departure, '%d.%m.%y %H:%M')
                stop =  Stop(station, arriveTime,departureTime)
                stops.append(stop)
                i += 1
                if i == len(lines):
                    break
                t = lines[i]
                train, station, arrive, departure, tmp = t.split(';')

            self.trains.append(Train(stops,500,100, id))
            #i += 1

        self.graph = RailGraph(dir+'/roads')


        #read constraints


        self.hard_constraints.append(constraints.MaxLengthConstraint)
        self.hard_constraints.append(constraints.MaxMassConstraint)
        self.hard_constraints.append(constraints.StraightRoadConstraint)
        self.soft_constraints.append(constraints.DelayConstraint)

    def constructInitialSolution(self):

        initial_trains = self.trains.copy()
        initial_unassigned_orders = self.orders.copy()

        sort_order = sorted(initial_unassigned_orders, key=lambda x : x.getPriority(), reverse= True)

        for job in sort_order:
            best_train = None
            best_cost = None
            for train in initial_trains:
                res = self.fulfilledHardConstraints(train,job)
                #print(res)
                if res == constraints.Status.NOT_FULFILLED:
                    continue
                insertion_cost = self.calculateInsertionCost(train, job)

                if insertion_cost is not None and (best_cost is None or insertion_cost < best_cost):
                    best_cost = insertion_cost
                    best_train = train

            if best_cost is not None:
                best_train.addActivity(job, job.getNumber())
                initial_unassigned_orders.remove(job)
            else:
                self.bad_jobs.append(job)
                print("Coudn't find direct train for job", job)
                print(self.graph.find_all_paths(job.getOrigin(), job.getDestination()))




        return Solution(initial_trains, initial_unassigned_orders)


    def calculateInsertionCost(self, train, job):
        cost = 0
        for const in self.soft_constraints:
            cost += const.cost(train, job)


        return cost


    def runAlgorithm(self):
        print("Construct initial solution")
        best_solution = self.constructInitialSolution()
        print(best_solution.calculateCost())
        best_solution.printSolution()
        bad = self.bad_jobs.copy()
        for order in bad:
            paths = self.graph.find_all_paths(order.getOrigin(), order.getDestination(),[])
            #print(paths)
            max_lengtn = max([len(x) for x in paths])
            print(order)
            for i in range(1, max_lengtn):
                best_trains = []
                best_cost = None
                for path in paths:
                    paths_split = self.split_path(path, i+1)

                    for parts in paths_split:
                        fuilfulledTrains = self.fulfilled(parts,order)
                        # print("__________")
                        # print(parts)
                        # for t in fuilfulledTrains:
                        #     print("trains")
                        #     for train in t:
                        #         print(train.id)
                        better_train_for_parts, cost = self.findBetterTrain(fuilfulledTrains, order, parts)
                        # print("better")
                        # for t in better_train_for_parts:
                        #     print(t.id)
                        # print(cost)

                        if best_cost is None:
                            best_cost = cost
                            best_trains = better_train_for_parts.copy()
                            best_parts = parts
                        else:
                            if cost is not None:
                                if best_cost > cost:
                                    best_cost = cost
                                    best_trains = better_train_for_parts.copy()
                                    best_parts = parts

                if best_cost is not None:
                    for t in best_trains:
                        print(t.id)
                    print(best_cost)
                    print(best_parts)
                    self.make_delivery(best_trains,order,best_parts)
                    self.bad_jobs.remove(order)
                    break

        print("Iterations end")
        print("best solution")
        solution = Solution(self.trains, self.bad_jobs)
        solution.printSolution()

    def fulfilledHardConstraints(self, train, order):
        partial = []
        for const in self.hard_constraints:
            if const.fulfilled(train, order) == constraints.Status.NOT_FULFILLED:
                return constraints.Status.NOT_FULFILLED

            if const.fulfilled(train, order) == constraints.Status.PARTIALY_FULFIELD:
                partial.append(const)


        if len(partial) == 0:
            return constraints.Status.FULFILLED
        else:
            return constraints.Status.PARTIALY_FULFIELD

    def split_path(self, path, param):


        if param > len(path):
            return []

        m = []
        for i in range(len(path)):
            m.append(0)
        m[0] = 1
        part_indexes =  self.bab(m,param,[])  #[x for x in self.bab(m,param,[]) if max(x) == param]

        parts = []
        for indexes in part_indexes:


            part = []
            p = []
            j = 1
            i = 0
            while i != len(indexes):
                if indexes[i] == j:
                    p.append(path[i])
                    i += 1
                else:
                    part.append(p)
                    p = []
                    j += 1
            part.append(p)

            if len(part[0]) == 1:
                continue
            for i in range(1,len(part)):
                part[i].insert(0,part[i-1][-1])

            parts.append(part)

        return parts


    def bab(self, m,n, paths = []):
        k = max(m)
        if k == n:
            for i in range(len(m)):
                if m[i] == 0:
                    m[i] = k

            paths.append(m.copy())
            return paths

        for i in range(len(m)):
            if m[i] == 0:
                m[i] = k
                paths = self.bab(m,n,paths)
                m[i] = k+1
                paths = self.bab(m,n,paths)
                m[i] = 0
                return paths
        return paths

    def fulfilled(self, parts, order):
        part_orders = []
        for part in parts:
            part_orders.append(Unit(order.id, order.getPriority(),order.getDueDate(),order.getMass(),order.getLength(),part[0], part[-1]))

        part_trains = []
        for part_order in part_orders:
            fulfilledTrains = []
            for train in self.trains:

                if self.fulfilledHardConstraints(train, part_order) == constraints.Status.FULFILLED:
                    fulfilledTrains.append(train)

            part_trains.append(fulfilledTrains)


        return part_trains

    def findBetterTrain(self, fuilfulledTrains, order, parts):
        part_orders = []
        for part in parts:
            part_orders.append(Unit(order.id,order.getPriority(),order.getDueDate(),order.getMass(),order.getLength(),part[0], part[-1]))

        roads = [[x] for x in fuilfulledTrains[0]]
        fuilfulledTrains.pop(0)
        while len(fuilfulledTrains) != 0:
            x = roads.copy()
            y = fuilfulledTrains[0]
            fuilfulledTrains.pop(0)
            roads.clear()
            for i in x:
                for j in y:
                    roads.append(i+[j])

        best_cost = None
        best_road = []

        for road in roads:
            if len(set(road)) != len(road):
                continue
            if self.canDeliver(road, order, parts):
                cost = self.calculateInsertionCost(road[-1], order)
                if best_cost is None:
                    best_cost = cost
                    best_road = road
                if best_cost > cost:
                    best_cost = cost
                    best_road = road


        return best_road, best_cost

    def canDeliver(self, road, order, parts):

        part_orders = []
        for part in parts:
            part_orders.append(Unit(order.id,order.getPriority(),order.getDueDate(),order.getMass(),order.getLength(),part[0], part[-1]))

        start_time = road[0].getTime(part_orders[0].getDestination())
        for i in range(1,len(road)):
            train = road[i]
            if train.getTime(part_orders[i].getOrigin()) < start_time:
                return False

        return True

    def make_delivery(self, best_trains, order, parts):
        part_orders = []
        for part in parts:
            part_orders.append(Unit(order.id, order.getPriority(),order.getDueDate(),order.getMass(),order.getLength(),part[0], part[-1]))

        for i in range(len(parts)):
            train = best_trains[i]
            order = part_orders[i]
            train.addActivity(order, 1)


Algorithm('test1').runAlgorithm()




