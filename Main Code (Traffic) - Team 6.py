# These modules will help us showcase our graph and help with Dijkstra's algorithm
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# This class will define intersections
class Intersection:
    # This will construct an intersection,
    # which needs at least two roads for it to be an intersection.
    # An intersection isn't one without two roads, but a road is a road
    # regardless of intersections.
    def __init__(self, ID, roadOne, roadTwo):
        self.__ID = ID

        # An intersection can intersect a maximum of 4 roads and a minimum of 2 (edges)
        # Here our nodes can be connected to a maximum of 4 edges
        # Because of that, we will define them as None (the other two)
        # Here we put all the roads in a list for easy access
        # But first we make sure we can add the roads to the intersection
        if roadOne.addIntersection(self) == False:
            roadOne = None
        if roadTwo.addIntersection(self) == False:
            roadTwo = None
        self.__roads = [roadOne, roadTwo, None, None]
        # This will be used for houses that need delivery
        self.__houses = set()


    # Setter/Getter functions
    def getID(self):
        return self.__ID
    def setID(self, ID):
        self.__ID = ID

    # Here we add/remove roads from an intersection
    def addRoad(self, road):
        # First we check if a road can be added
        if None in self.__roads:
            # Then we check if the road has an empty space for the intersection
            # This will add the intersection if the road has an empty space
            if road.addIntersection(self) == False:
                return "Can't add road to intersection, not empty space available"

            # We go through every road and replace the empty space with the new road
            for roadNum in range(len(self.__roads)):
                if self.__roads[roadNum] == None:
                    self.__roads[roadNum] = road
                    return "Road added successfully"
        return "Road can't be added to the intersection, max number of roads reached."
    def removeRoad(self, road):
        # We remove the road if it is connected to the intersection
        if road in self.__roads and road != None:
            # We remove the intersection from the road object
            road.removeIntersection(self)
            for roadNum in range(len(self.__roads)):
                if self.__roads[roadNum] == road:
                    # Keep in mind, we replace it with None because an intersection has a maximum
                    # of 4 roads.
                    self.__roads[roadNum] = None
        return "Road has been removed"

    # This helps us replace a road with another
    def replaceRoad(self, roadReplaced, road):
        self.removeRoad(roadReplaced)
        self.addRoad(road)

    # This returns the list of roads
    def getRoads(self):
        return self.__roads

    # To add/remove houses from the intersection
    def addHouse(self, house):
        # We are using a set for houses, so we don't need to worry about duplicates
        self.__houses.add(house)
        # Now we update the house's location
        house.setLocation(self)
    def removeHouse(self, house):
        # First we check if the house is near the intersection or not
        if house in self.__houses:
            self.__houses.remove(house)
        # Now we update the house's location
        house.setLocation(None)

    # To get houses
    def getHouses(self):
        return self.__houses

    # To find the shortest distance between two roads
    # This will be used for dijkstra algorithm
    def shortestRoad(self):
        # This will check the length of each road if available
        # Then return the list of roads and the distance in each
        # We will also get the destination from that road
        edges = self.__roads
        roadLengths = []
        destinations = []
        for i in range(len(edges)):
            if edges[i] != None:
                for posDest in edges[i].getIntersections():
                    if posDest != self and posDest != None:
                        roadLengths.append(edges[i].getLength())
                        destinations.append(posDest)
        return destinations, roadLengths

    # To display intersection details:
    def displayIntersection(self):
        print(f"Intersection ID: {self.getID()}")
        print(f"Roads: ")
        if self.getRoads() == [None, None, None, None]:
            print("NO ROADS ARE CONNECTED")
            return
        for road in self.getRoads():
            if road != None:
                print(f"Road name: {road.getName()}")
                print(f"Road ID: {road.getID}")
                return
        print("Houses near intersection: ")
        for house in self.getHouses():
            print(f"House ID: {house.getID()}")

# This class will define roads
class Road:
    # This constructs a road
    def __init__(self, ID, name, length, traffic_status):
        self.__ID = ID
        self.__name = name
        self.__length = length
        # This will be used to generate approximated time to go through this road
        # but in this implementation it won't be a variable for showcasing simplicity
        self.__traffic = traffic_status

        # Here a road will connect two intersections at most
        self.__intersections = [None, None]

    # Setter/Getter functions
    def getID(self):
        return self.__ID
    def setID(self, ID):
        self.__ID = ID
    def getName(self):
        return self.__name
    def setName(self, name):
        self.__name = name
    def getLength(self):
        return self.__length
    def setLength(self, length):
        self.__length = length
    def getTraffic(self):
        return self.__traffic
    def setTraffic(self, traffic_status):
        self.__traffic = traffic_status

    # To add/remove intersections
    def addIntersection(self, intersection):
        # Check if there is an empty space
        if None in self.__intersections:
            for intersectionNum in range(len(self.__intersections)):
                if self.__intersections[intersectionNum] == None:
                    self.__intersections[intersectionNum] = intersection
                    return True
        return False
    def removeIntersection(self, intersection):
        if intersection in self.__intersections:
            for intersectionNum in range(len(self.__intersections)):
                if self.__intersections[intersectionNum] == intersection:
                    self.__intersections[intersectionNum] = None
        return True

    # This is to get the list of intersections connected to the road
    def getIntersections(self):
        return self.__intersections

    # To display the road
    def displayRoad(self):
        print(f"Road name: {self.getName()}")
        print(f"Road ID: {self.getID()}")
        print("Intersections: ")
        if self.getIntersections() == [None, None]:
            print("NO INTERSECTIONS ARE CONNECTED")
            return
        for intersection in range(len(self.getIntersections())):
            if intersection != None:
                print(f"Intersection: {self.__intersections[intersection].getID()}")
                return


# Class for houses to send packages to
class House:
    # Contract the house and give it a location
    # In this case we will connect houses to intersection
    def __init__(self, ID, intersection):
        self.__ID = ID
        self.__location = intersection
        if intersection != None:
            intersection.addHouse(self)

    # Setter/getter functions
    def getID(self):
        return self.__ID
    def setID(self, ID):
        self.__ID = ID
    def getLocation(self):
        return self.__location
    def setLocation(self, intersection):
        self.__location = intersection

    # To display house details
    def displayHouse(self):
        print(f"House ID: {self.getID()}")
        print(f"Location (Nearest intersection): {self.getLocation()}")


# This will represent the traffic network
class TrafficNetwork:
    # Since the whole system is connected via roads
    # One intersection could use the roads connected to it to represent and draw the system
    # So we will have one intersection as the parameter, then the code will do the rest
    def __init__(self, networkName, intersection):
        self.__networkName = networkName
        # We will make our nodes/intersections and edges/roads in a set so no duplicates appear
        # We will also add a set for houses
        self.__trafficIntersections = set()
        self.__trafficRoads = set()
        self.__trafficHouses = set()

        self.__trafficIntersections.add(intersection)
        # This queue will save us from running into errors while iterating
        queue = [intersection]

        # This will use that one intersection to add every other intersection
        # via traversing the roads.
        # Since no duplicates are on the set, we won't go through intersections twice
        for intersections in queue:
            # We will first add the houses to the traffic network
            # then we traverse the roads
            for houses in intersections.getHouses():
                self.__trafficHouses.add(houses)
            for roads in intersections.getRoads():
                # We get the road's intersections and add new ones.
                # We will also add roads while doing this
                if roads != None:
                    # We filter None
                    self.__trafficRoads.add(roads)
                    for roadIntersections in roads.getIntersections():
                        if roadIntersections != None:
                            # We filter None
                            self.__trafficIntersections.add(roadIntersections)
                            # Add to the queue
                            if roadIntersections not in queue:
                                queue.append(roadIntersections)

    # Setter/getter functions
    def getNetworkName(self):
        return self.__networkName
    def setNetworkName(self, name):
        self.__networkName = name

    # To add/remove intersections to the network
    def addIntersection(self, intersection):
        # Since we are using sets we don't have to worry about duplicates
        self.__trafficIntersections.add(intersection)
        # We will also add the associated roads
        for road in intersection.getRoads():
            if road != None:
                # We filter out None
                self.__trafficRoads.add(road)
        # We also add traffic houses to the system
        for house in intersection.getHouses():
            self.__trafficHouses.add(house)
    def removeIntersection(self, intersection):
        # Since roads still depend on other intersections we will only remove the intersection
        # But we will make sure the intersection isn't connected to the road anymore
        # We will check if the intersection exists to avoid errors
        # We also remove houses associated with this intersection
        if intersection in self.__trafficIntersections:
            self.__trafficIntersections.remove(intersection)
            for road in intersection.getRoads():
                intersection.removeRoad(road)
            for house in intersection.getHouses():
                self.__trafficHouses.remove(house)
        return True

    # To get traffic intersections
    def getIntersections(self):
        return self.__trafficIntersections

    # To add/remove roads
    def addRoad(self, road):
        # Again we are using sets, we don't have to worry about duplicates
        self.__trafficRoads.add(road)
    def removeRoad(self, road):
        # We check if the road exist to avoid errors
        if road in self.__trafficRoads:
            self.__trafficRoads.remove(road)
        return True

    # To get traffic roads
    def getRoads(self):
        return self.__trafficRoads

    # To add/remove and get houses
    def addHouse(self, house):
        # We are using a set for houses, so we don't need to worry about duplicates
        self.__trafficHouses.add(house)
    def removeHouse(self, house):
        # First we check if the house is near the intersection or not
        if house in self.__trafficHouses:
            self.__trafficHouses.remove(house)
    # To get houses
    def getHouses(self):
        return self.__trafficHouses


    # Dijkstra algorithm for shortest route to houses
    def dijkstra(self, current):
        # This dictionary holds the shortest distance from our current location.
        # The previous dictionary holds the previous intersection to help us get
        # To the designated intersection in the shortest distance possible.
        distances = {node.getID(): float('inf') for node in self.__trafficIntersections}
        previous = {node.getID(): None for node in self.__trafficIntersections}
        houses = {}
        distances[current.getID()] = 0

        # To keep track of visited nodes/intersections
        visited = set()

        # Priority queue for visiting unvisited nodes
        pq = [(0, current)]

        # Now we keep going until the queue is empty, this will make sure we went through every node
        while pq:
            # Pop the node with the smallest distance
            currentLength, current = heapq.heappop(pq)

            # Skip if already visited
            if current in visited:
                continue

            # Mark current node as visited
            visited.add(current)

            # We retrieve the destinations from the current node and their length
            destinations, roadLengths = current.shortestRoad()

            # Update distances and previous for each destination based on current and new distance
            for destination, length in zip(destinations, roadLengths):
                # Calculate new distance
                new_distance = distances[current.getID()] + length

                # If the new distance is shorter, update distances, previous, and houses
                if new_distance < distances[destination.getID()]:
                    distances[destination.getID()] = new_distance
                    previous[destination.getID()] = current.getID()
                    houses[destination.getID()] = len(destination.getHouses())


                    # Push the destination to the priority queue with its updated distance
                    heapq.heappush(pq, (new_distance, destination))


        # Sort the dictionaries based on intersection IDs
        sorted_distances = dict(sorted(distances.items()))
        sorted_previous = dict(sorted(previous.items()))
        sorted_houses = dict(sorted(houses.items()))

        return sorted_distances, sorted_previous, sorted_houses


    # To distribute packages
    def packageDistribution(self, distances, houses_count):
        # Combine distances and houses count into a single dictionary for each intersection
        intersections_info = {intersection_id: (distances[intersection_id], houses_count.get(intersection_id, 0)) for
                              intersection_id in distances}

        # Sort intersections based on distance and then by the number of houses
        sorted_intersections = sorted(intersections_info.items(), key=lambda x: (x[1][0], -x[1][1]))

        # Extract the sorted intersection IDs
        sorted_intersection_ids = [intersection_id for intersection_id, _ in sorted_intersections]

        # Return the sorted intersections
        return sorted_intersection_ids

    # To initialize the graph
    # Every time the network changes we need to initialize it for optimal results
    def initializeNetwork(self):
        # We are going to create the graph using networkx and matplotlib
        self.__G = nx.Graph()
        # Now we add the intersections as nodes but will make sure their ID is outputted
        nodes = []
        for node in self.__trafficIntersections:
            nodes.append(node.getID())

        # Now we add them as nodes
        self.__G.add_nodes_from(nodes)

        # Next we add the edges
        edges = []
        for edge in self.__trafficRoads:
            # Here we add the two intersections connected and the length of the road as a tuple
            # But we filter out edges that don't connect two nodes
            # This temp list will hold intersection for this specific road
            temp = edge.getIntersections()
            if None not in temp:
                edges.append((temp[0].getID(), temp[1].getID(), edge.getLength()))

        # Now we add the edges
        self.__G.add_weighted_edges_from(edges)

    # To show the network
    def showNetwork(self):
        # Choose a different layout algorithm for better spacing
        pos = nx.spring_layout(self.__G, seed=42)

        # Increase the figure size for better visibility
        plt.figure(figsize=(10, 8))

        # Draw the graph with edge weights
        nx.draw(self.__G, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=12, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.__G, 'weight')
        nx.draw_networkx_edge_labels(self.__G, pos, edge_labels=edge_labels)

        # Display the graph
        plt.show()


# Test cases:
# First we will create 22 roads
road1 = Road("01", "Andrew Road", 2000, "Normal")
road2 = Road("02", "IDK Road", 1500, "Normal")
road3 = Road("03", "Mohammed Road", 1750, "Normal")
road4 = Road("04", "Speed Road", 10000, "Normal")
road5 = Road("05", "Godzilla Road", 1900, "Normal")
road6 = Road("06", "Kong Road", 1800, "Normal")
road7 = Road("07", "DON'T SPEED Road", 15000, "Normal")
road8 = Road("08", "Cold Road", 2200, "Normal")
road9 = Road("09", "Warm Road", 2250, "Normal")
road10 = Road("10", "Andre Road", 3000, "Normal")
road11 = Road("11", "Dot Road", 3500, "Normal")
road12 = Road("12", "Cole Road", 2700, "Normal")
road13 = Road("13", "Running Out of Names Road", 2800, "Normal")
road14 = Road("14", "Some Name Road", 2850, "Normal")
road15 = Road("15", "X Road", 2900, "Normal")
road16 = Road("16", "Y Road", 1500, "Normal")
road17 = Road("17", "Z Road", 2000, "Normal")
road18 = Road("18", "Poke Road", 2100, "Normal")
road19 = Road("19", "R6 Road", 1750, "Normal")
road20 = Road("20", "Final Road", 17000, "Normal")
road21 = Road("20", "Extra Road", 3100, "Normal")
road22 = Road("20", "Final 2 Road", 18000, "Normal")


# Now we create 20 intersections using the roads we have
intersection1 = Intersection("01", road1, road2)
intersection2 = Intersection("02", road2, road3)
intersection3 = Intersection("03", road3, road4)
intersection4 = Intersection("04", road13, road5)
intersection5 = Intersection("05", road5, road4)
intersection6 = Intersection("06", road6, road7)
intersection7 = Intersection("07", road7, road8)
intersection8 = Intersection("08", road8, road9)
intersection9 = Intersection("09", road9, road10)
intersection10 = Intersection("10", road10, road11)
intersection11 = Intersection("11", road11, road12)
intersection12 = Intersection("12", road12, road6)
intersection13 = Intersection("13", road12, road1)
intersection14 = Intersection("14", road13, road14)
intersection15 = Intersection("15", road15, road14)
intersection16 = Intersection("16", road16, road15)
intersection17 = Intersection("17", road16, road17)
intersection18 = Intersection("18", road18, road20)
intersection19 = Intersection("19", road19, road18)
intersection20 = Intersection("20", road18, road17)

# Now we will add the remaining roads to the intersections
intersection18.addRoad(road21)
intersection5.addRoad(road22)
intersection3.addRoad(road21)
intersection10.addRoad(road22)

# Add houses to the system so we can test the package distribution system
house1 = House("001", intersection1)
house2 = House("002", intersection1)
house3 = House("003", intersection10)
house4 = House("004", intersection10)
house5 = House("005", intersection10)
house6 = House("006", intersection20)
house7 = House("007", intersection17)
house8 = House("008", intersection7)
house9 = House("009", intersection18)
house10 = House("010", intersection15)


# Now we will initialize and show the network
# As you can see, the network has 20 intersections
# If the image is too cramped use the magnifying glass to look closer
trafficSystem1 = TrafficNetwork("Andrew City", intersection1)

# Here we get the shortest path from a node to every other node
# We will also print out the order of distributing packages from this info
distances, previous, houses_count = trafficSystem1.dijkstra(intersection20)
print(f"Shortest distances (from intersection 20): {distances}\n")
print(f"Shortest distance order (from intersection 20): {previous}\n")
print(f"Number of houses in each intersection: {houses_count}\n")
print(f"Order of package distribution: {trafficSystem1.packageDistribution(distances, houses_count)}\n")
print(f"Based on our distances it makes sense intersection 10 is the last because it is the furthest away. "
      f"Even if it did have the largest number of packages it is the furthest and we can distriubte more if we leave it last.")

trafficSystem1.initializeNetwork()
trafficSystem1.showNetwork()


# Now we will try to remove two intersection, add one, change the distance between node 10 and 5,
# and start from another node.

# Let's try removing intersection 7
trafficSystem1.removeIntersection(intersection7)

# Change the distance between node 10 and 5 (road 22)
road22.setLength(1050)

# Add a node to connecting to intersection 19
intersection21 = Intersection("21", road19, road18)

# Create a new road and use it to connect a new intersection to intersection 3
# Lets add a package there to the new intersection
road23 = Road("20", "Vince Road", 1000, "Normal")

# Connect the road to intersection 3
intersection3.addRoad(road23)

# Create the new intersection and add a house to it
intersection22 = Intersection("22", road23, road19)
house11 = House("011", intersection22)

# Now let's add the intersections to the system
trafficSystem1.addIntersection(intersection21)
trafficSystem1.addIntersection(intersection22)


# Finally, we generate a new shortest distance and distribute packages from there
# We will choose intersection 13 this time
distances, previous, houses_count = trafficSystem1.dijkstra(intersection13)
print(f"Shortest distances (from intersection 20): {distances}\n")
print(f"Shortest distance order (from intersection 20): {previous}\n")
print(f"Number of houses in each intersection: {houses_count}\n")
print(f"Order of package distribution: {trafficSystem1.packageDistribution(distances, houses_count)}\n")
print(f"You notice the this time, when reached node 03, we went to 22 first then 18.")
print(f"This tells us our system works perfectly fine because it is faster to go to intersection 22 then to 18.")
print(f"Moreover, out system looks different and the length between node 10 and node 5 changed")

# Lastly, we display our new traffic network
# We see that the system works perfectly fine
trafficSystem1.initializeNetwork()
trafficSystem1.showNetwork()