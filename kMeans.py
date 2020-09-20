from sklearn.cluster import KMeans
import numpy as np
from math import degrees, atan2, sqrt
import savings
import util



# This function calculates the angle of the customer with the depot
def calculateDepotAngle(x,y,depot_x,depot_y):
    angle = degrees(atan2(y - depot_y, x - depot_x))
    bearing = (90 - angle) % 360
    return bearing

def euclideanDistance( xy1, xy2 ):
    "Returns the Euclidean distance between points xy1 and xy2"
    return  (( xy2[0] - xy1[0] )**2 + ( xy2[1] - xy1[1] )**2)

# The input locations and the demands
locations = [(15, 19),(1 ,49),(87, 25),(69, 65),(93, 91),(33, 31),(71, 61),(29, 9),(93, 7),
                (55, 47),(23, 13),(19, 47),(57, 63),(5 ,95),(65, 43),(69, 1),(3 ,25),(19, 91),
                (21, 81),(67, 91),(41, 23),(19, 75),(15, 79),(79, 47),(19, 65),(27, 49),(29, 17),
                (25, 65),(59, 51),(27, 95),(21, 91),(61, 83),(15, 83),(31, 87),(71, 41),(91, 21)]

demands = [0, 1, 14, 15, 11, 18, 2, 22, 7, 18, 23, 12, 21, 2, 14, 9, 10, 4, 19, 2, 20, 15,
                 11, 6, 13, 19, 13, 8, 15, 18, 11, 21, 12, 2, 23, 11]
# Initial number of clusters to be formed
noOfClusters = 5

# The capacity of the vehicles
VehicleCapacity = 100

# n37-k6 NEO
# locations = [(86, 22),(29, 17),(4, 50),(25, 13),(67, 37),(13, 7),(62, 15),(84, 38),(34, 3),
#             (19, 45),(42, 76),(40, 86),(25, 94),(63, 57),(75, 24),(61, 85),(87, 38),(54, 39),
#             (66, 34),(46, 39),(47, 17),(21, 54),(19, 83),(1, 82),(94, 28),(82, 72),(41, 59),
#             (100, 77),(1, 57),(96, 7),(57, 82),(47, 38),(68, 89),(16, 36),(51, 38),(83, 74),(84, 2)]

# demands = [0, 1, 23, 23, 5, 7, 18, 12, 20, 19, 19, 16, 2, 26, 13, 19, 17, 14, 8, 10, 5,
#              19, 12, 9, 18, 4, 20, 8, 3, 18, 26, 21, 21, 8, 19, 66, 21]
# # Initial number of clusters to be formed
# noOfClusters = 7

# # n45-k6 NEO
# locations = [(31, 73),(11, 67),(52, 96),(81, 29),(97, 62),(71, 5),(6, 56),(48, 50),(91, 17),
#             (49, 68),(85, 29),(11, 16),(74, 98),(56, 37),(13, 81),(66, 80),(96, 55),(36, 17),
#             (32, 23),(6, 13),(64, 30),(87, 5),(75, 61),(40, 72),(1, 44),(60, 95),(27, 49),
#             (15, 33),(46, 53),(28, 43),(3, 9),(1, 100),(53, 46),(98, 8),(6, 25),(7, 81),(96, 88),
#             (2, 35),(32, 94),(95, 94),(9, 11),(96, 16),(90, 68),(33, 31),(6, 59)]

# demands = [0 ,19 ,2 ,12 ,20 ,6 ,17 ,8 ,14 ,2 ,8 ,5 ,7 ,22 ,14 ,17 ,23 ,15 ,21 ,2 ,24 ,10 ,20 ,
#             6 ,21 ,10 ,6 ,13 ,21 ,24 ,11 ,16 ,8 ,11 ,11 ,22 ,17 ,22 ,17 ,8 ,23 ,5 ,3 ,18 ,12 ]
# # # Initial number of clusters to be formed
# noOfClusters = 7

# The capacity of the vehicles
# VehicleCapacity = 100

# 75 nodes - fruity bun
# locations = [(40,40) ,(22,22) ,(36,26) ,(21,45) ,(45,35) ,(55,20) ,(33,34) ,(50,50) ,(55,45) ,
#                 (26,59) ,(40,66) ,(55,65) ,(35,51) ,(62,35) ,(62,57) ,(62,24) ,(21,36) ,(33,44) ,(9,56) ,
#                 (62,48) ,(66,14) ,(44,13) ,(26,13) ,(11,28) ,(7,43) ,(17,64) ,(41,46) ,(55,34) ,(35,16) ,
#                 (52,26) ,(43,26) ,(31,76) ,(22,53) ,(26,29) ,(50,40) ,(55,50) ,(54,10) ,(60,15) ,
#                 (47,66) ,(30,60) ,(30,50) ,(12,17) ,(15,14) ,(16,19) ,(21,48) ,(50,30) ,(51,42) ,(50,15) ,
#                 (48,21) ,(12,38) ,(15,56) ,(29,39) ,(54,38) ,(55,57) ,(67,41) ,(10,70) ,(6,25) ,      
#                 (65,27) ,(40,60) ,(70,64) ,(64,4) ,(36,6) ,(30,20) ,(20,30) ,(15,5) ,(50,70) ,(57,72) ,
#                 (45,42) ,(38,33) ,(50,4) ,(66,8) ,(59,5) ,(35,60) ,(27,24) ,(40,20) ,(40,37)]

# demands = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,
#             18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,
#             12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]

# # # # Initial number of clusters to be formed
# noOfClusters = 15

# # The capacity of the vehicles
# VehicleCapacity = 220

# Storing the Depot coordinates
DepotX = locations[0][0]
DepotY = locations[0][1]

totalDistance = 0
while len(locations) > 1:
	print(len(locations), noOfClusters)

	# Making an array of locations of the customer coordinates
	npLocations = np.array(locations[1:])
	npDemands = np.array(demands[1:])

	# This variable stores the number of customers still left to be served by any vehicle.
	# Initially it is equal to the number of customers
	locationsLeftToServe = len(npDemands)
	noOfClusters = min(noOfClusters, locationsLeftToServe)

	# Calling the KMeans function for clustering 
	kmeans = KMeans(n_clusters=noOfClusters, random_state=0).fit(npLocations)
	# print(kmeans.cluster_centers_)

	# Storing the centers of the clusters
	clusterCenter = kmeans.cluster_centers_
	# print(kmeans.labels_)
	clusterLabel = kmeans.labels_

	# Calculating the angle that the cluster center makes with the depot
	anglesOfClusterCenters = []
	for i in range(0, noOfClusters):
		anglesOfClusterCenters.append(calculateDepotAngle(clusterCenter[i][0], clusterCenter[i][1], DepotX, DepotY))
	# print(anglesOfClusterCenters)



	# Finding the cluster which makes the least angle with the depot
	currentCluster = 0
	minAngle = 361
	for i in range(noOfClusters):
		if anglesOfClusterCenters[i] < minAngle:
			minAngle = anglesOfClusterCenters[i]
			currentCluster = i
	# print(currentCluster)

	# Finding the total sum of demands in the current cluster
	sumOfDemands = 0
	for i in range(locationsLeftToServe):
		if clusterLabel[i] == currentCluster:
			sumOfDemands = sumOfDemands + npDemands[i]

	# print(sumOfDemands)

	clustersLeft = noOfClusters - 1
	currentSetOfClusters = set()
	currentSetOfClusters.add(currentCluster)

	while clustersLeft > 1 and sumOfDemands < VehicleCapacity:
		
		# Find the cluster closest to the current cluster
		clusterIndex = 0
		minDistance = 100000000
		for i in range(noOfClusters):
			if i in currentSetOfClusters:
				continue
			curDistance = euclideanDistance(clusterCenter[currentCluster], clusterCenter[i])
			if curDistance < minDistance:
				minDistance = curDistance
				clusterIndex = i

		clustersLeft = clustersLeft - 1
		currentSetOfClusters.add(clusterIndex)
		for i in range(locationsLeftToServe):
			if clusterLabel[i] == clusterIndex:
				sumOfDemands = sumOfDemands + npDemands[i]
	# print(currentSetOfClusters)

	customerPosDemand = dict()
	for i in range(locationsLeftToServe):
		for c in currentSetOfClusters:
			if clusterLabel[i] == c:
				customerPosDemand[npLocations[i][0], npLocations[i][1]] = npDemands[i]
				
	# print(customerPosDemand)
	
	custIndex = []
	routes = savings.func(customerPosDemand, (DepotX, DepotY))

	print("Routes = ", routes)
	for k,v in routes.iteritems():
		totalDistance += util.calculateRouteCost(v)
		numCust = len(v)
		for i in range(1,numCust-1):
			wh = locations.index(v[i])
			custIndex.append(wh-1)

			val = np.array(v[i])
			# print(np.where(npLocations == val))
		# print(k,'-',v)

	# print(locations)
	# print(custIndex)
	# print(totalDistance)

	# print(len(npLocations))
	# print(len(npDemands))

	npLocations = np.delete(npLocations, custIndex, 0)
	npDemands = np.delete(npDemands, custIndex, 0)

	# print(len(npLocations))
	# print(len(npDemands))

	# locations = npLocations.tolist()
	# demands = npDemands.tolist()
	del locations[:]
	del demands[:]

	# locations.append((DepotX, DepotY))

	for x in npLocations:
		locations.append((x[0], x[1]))

	for x in npDemands:
		demands.append(x)

	locations.insert(0, (DepotX, DepotY))
	demands.insert(0, 0)
	noOfClusters = noOfClusters - 1

print(totalDistance)