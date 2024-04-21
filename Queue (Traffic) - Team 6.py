class Queue:
    def __init__(self):
        self.queue = []

    def pushPackage(self, house):
        self.queue.append(house)

    def cancelPackage(self, house):
        if house in self.queue:
            self.queue.remove(house)
            return True
        return False

    def processPackage(self):
        if self.queue:
            nextPackage = self.queue.pop(0)
            return nextPackage
        else:
            print("No packages in the queue.")


# Test Cases (example of usage):

# First we will add 5 houses that need to distribute packages to
house1 = "House 01"
house2 = "House 02"
house3 = "House 03"
house4 = "House 04"
house5 = "House 05"

# Then we create the queue and push the houses into the queue
packageDistribution = Queue()

packageDistribution.pushPackage(house1)
packageDistribution.pushPackage(house2)
packageDistribution.pushPackage(house3)
packageDistribution.pushPackage(house4)
packageDistribution.pushPackage(house5)
print(f"Queue at the beginning: {packageDistribution.queue}")

# Now lets try to deque three times
print (packageDistribution.processPackage())
print (packageDistribution.processPackage())
print (packageDistribution.processPackage())

# Lets check the current queue and try adding two more packages and cancel one
print(f"Current queue: {packageDistribution.queue}")

house6 = "House 06"
house7 = "House 07"
packageDistribution.pushPackage(house6)
packageDistribution.pushPackage(house7)
packageDistribution.cancelPackage(house5)
print(f"Queue after adding two packages and canceling one: {packageDistribution.queue}")

# Now lets try to deque until we cant anymore
print (packageDistribution.processPackage())
print (packageDistribution.processPackage())
print (packageDistribution.processPackage())
print (packageDistribution.processPackage())
print(f"Our package distribution process in a neighbourhood works as intended")