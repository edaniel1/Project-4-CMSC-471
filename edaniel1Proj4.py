# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:41:51 2016

@author: Daniel_2
"""

"""
Important!! The centroid that is used for the clustering
is show as a square. So the square in the plot is NOT a
real point. Instead it signifies the center of the cluster.
"""

from sys import argv
import random
import math
import matplotlib.pyplot as plt

def main():
    
    #inline arguments
    numClusters = int(argv[1])
    readFile = argv[2]
    #parses the file and stores it in graph
    graph = parseInFile(readFile)
    #creates initial centroids
    centroids = createCentroids(graph, numClusters)
    clusters = []
    
    #runs until flag set to false (when centroids dont change)
    flag = True
    while(flag):
        #assigns nodes to cluster (closest centroid)
        clusters = assignClusters(centroids, graph)
        #creates new centroids based on clusters
        newCentroids = averageCentroids(clusters)
        #if the centroids didnt change, end loop
        if(newCentroids == centroids):
            flag = False
        centroids = newCentroids
    
    #graphs the clusters and centroids
    graphData(clusters, centroids)
    

#parses each file
def parseInFile(readFile):
    
    inFile = open(readFile, "r")
    graph = []
    #turns each line into an ordered pair
    for line in inFile:
        pair = line.split()
        pair = [int(pair[0]), int(pair[1])]
        graph.append(pair)
    return graph


def createCentroids(graph, numClusters):
    #finds the min and max values for X and Y
    minX = min(map(lambda x: x[0], graph))
    maxX = max(map(lambda x: x[0], graph))
    minY = min(map(lambda x: x[1], graph))
    maxY = max(map(lambda x: x[1], graph))

    #creates random centroids based on the min and max values
    centroids = []
    i = 0
    while(i < numClusters):
        i += 1
        cenX = random.randrange(minX, maxX)
        cenY = random.randrange(minY, maxY)
        centroids.append([cenX, cenY])
    return centroids
    
def assignClusters(centroids, graph):
    
    clusters = []
    #sets up the clusters list
    for cent in centroids:
        clusters.append(cent)
        clusters.append([])
    #runs for each node
    for pair in graph:
        minDist = -1
        toCent = -1
        #compares each centroid to the node
        for cent in centroids:
            if(minDist != -1):
                #dist = distance between pair and cent
                dist = distance(pair[0], cent[0], pair[1], cent[1])
                if(dist < minDist):
                    minDist = dist
                    toCent = centroids.index(cent)
            else:
                minDist = distance(pair[0], cent[0], pair[1], cent[1])
                toCent = centroids.index(cent)
        #assigns node to cluster with the closest centroid
        clusters[toCent * 2 + 1].append(pair)
    return clusters
    
def averageCentroids(clusters):
    
    centroids = []
    i = 0
    while (i < len(clusters)):
        cluster = clusters[i+1]
        #sums each column in cluster (ex: [[1, 3], [2, 4]] - > [3, 7])
        clusterSum = [sum(i) for i in zip(*cluster)]
        #creates the average of each column as an ordered pair
        clusterAvg = [clusterSum[0]/len(clusters[i+1]), clusterSum[1]/len(clusters[i+1])]
        #the ordered pair becomes the new centroid
        centroids.append(clusterAvg)
        i += 2
    return centroids
    
def distance(Xa, Xb, Ya, Yb):
    #returns the distance betweent he nodes
    dist = math.sqrt( ((Xa-Xb) ** 2) + ((Ya-Yb) ** 2) )
    return dist
    
def graphData(clusters, centroids):

    noCentClusters = []
    #creates list of clusters without centroids
    i = 0
    while i < len(clusters):
        noCentClusters.append(clusters[i + 1])
        i += 2
    #swaps list of clusters from list of lists of ordered pairs to
    #   a list of lists with a list of x values and a list y values
    #this is needed for graphing
    swapNoCentClusters = []
    c = 0
    for cluster in noCentClusters:
        swapNoCentClusters.append([[],[]])
        for pair in cluster:
            swapNoCentClusters[c][0].append(pair[0])
            swapNoCentClusters[c][1].append(pair[1])
        c += 1
    #swaps list of centroids from list of centroids to a list with a 
    #   list of x values and a list of y values
    #this is needed for graphing
    swapCentroids = [[],[]]
    for cent in centroids:
        swapCentroids[0].append(cent[0])
        swapCentroids[1].append(cent[1])
    #plots the clusters and centroids
    for cluster in swapNoCentClusters:
        plt.plot(cluster[0], cluster[1], 'o')
    plt.plot(swapCentroids[0], swapCentroids[1], 's')
    
    plt.show()
        
main()