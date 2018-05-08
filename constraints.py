import math

from unit import Unit

class Status:
    NOT_FULFILLED = "NOT_FULFILLED"
    FULFILLED = "FULFILLED"
    PARTIALY_FULFIELD = "PARTIALY_FULFIELD"


class HardConstraint:
    @staticmethod
    def fulfilled(train, order):
        return Status.NOT_FULFILLED


class SoftConstraint:
    @staticmethod
    def cost(train, order):
        return 0




class MaxMassConstraint(HardConstraint):
    @staticmethod
    def fulfilled(train, order):
        # if train.current_mass + order.getMass()/order.getNumber() > train.max_mass:
        #     return Status.NOT_FULFILLED
        train_current_mass = 0
        for activity in train.activities:
            if activity.type == "pickup":

                for o in activity.orders:
                    train_current_mass += o.getMass()

            if activity.type == "delivery":
                for o in activity.orders:
                    train_current_mass -= o.getMass()

            if activity.station == order.getOrigin():
                break
        if train_current_mass + order.getMass() > train.max_mass:
            return Status.NOT_FULFILLED
            #return Status.PARTIALY_FULFIELD

        return Status.FULFILLED



class MaxLengthConstraint(HardConstraint):
    @staticmethod
    def fulfilled(train, order):
        # if train.current_length + order.getLength()/order.getNumber() > train.max_length:
        #     return Status.NOT_FULFILLED
        train_current_length = 0

        for activity in train.activities:
            if activity.type == "pickup":

                for o in activity.orders:
                    train_current_length += o.getLength()

            if activity.type == "delivery":
                for o in activity.orders:
                    train_current_length -= o.getLength()

            if activity.station == order.getOrigin():
                break
        if train_current_length + order.getLength() > train.max_length:
            return Status.NOT_FULFILLED
            #return Status.PARTIALY_FULFIELD

        return Status.FULFILLED


class StraightRoadConstraint(HardConstraint):
    @staticmethod
    def fulfilled(train, order):
        origin = order.getOrigin()
        destination = order.getDestination()

        fromFlag = False
        toFlag = False
        for t in train.timetable:
            if int(t.station) == int(origin) and fromFlag == False:
                fromFlag = True

            if int(t.station) == int(destination) and fromFlag == True and toFlag == False:
                toFlag = True
                break

        if fromFlag == False or toFlag == False:
            return Status.NOT_FULFILLED

        return Status.FULFILLED

class DelayConstraint(SoftConstraint):
    @staticmethod
    def cost(train, order):
        destination = order.getDestination()
        return max(0,(train.getTime(destination)-order.getDueDate()).seconds/60)