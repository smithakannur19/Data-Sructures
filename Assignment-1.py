#!/usr/bin/env python
# coding: utf-8

# **Problem Statement** <br/>
# Assume you work for a start-up company whose business model is to make available local delicacies 
# across India. They work on the promise of same day delivery of food items across India and are trying 
# to build a logistical chain for the same which can deliver across Airports using their patented food 
# boxes which preserve the food quality within transit. Your team is tasked with developing a system 
# which can record all air cargo delivery routes that are available between airports in India. The data is 
# captured such that each cargo plane and its associated airports are captured as vertices and the 
# association as edges. Assume that the flights are bi-directional, that means the same cargo flight 
# number is used for the onward and return journey. 

# **Reading the data**

# def readAirportFlightfile(self, inputfile): This function reads the input file inputPS15.txt
# containing the name of the airport and the cargo flights between them in one line separated 
# by a slash. A sample input file entry is shown below. The flight number is the first entry in 
# each row followed by the different airports it services separated by a slash ‘/’ <br/><br/>
# indigo777 / Chennai / New Delhi <br/><br/>
# The function should create relevant vertices for both the cargo flights and its associated 
# airports and relevant edges to indicate the association of a flight and its connecting airports. 
# Ensure that the vertices are unique and there are no duplicates.
# 

# In[3]:


def readAirportFlightfile(inputfile):
    with open(inputfile, "r") as f:
        data = f.readlines()
    print("Read Data --> ", data)
    return data


# **List of unique cargo planes and list of unique airports that have delivery service.**

# def showAll(self): This function displays the count of unique cargo flights and airports 
# entered through the input file. It should also list out the unique cargo flights and airports that 
# have cargo service stored. This function is called after all input data has been captured. The 
# output of this function should be pushed into outputPS15.txt file. The output format should 
# be as mentioned below. 

# In[5]:


def showAll(data):
    graph = {}
    for i in data:
        i = i.split("/")
        i = list(map(str.strip, i))
        if "" in i:
            i.remove("")
        if len(i) != 0:
            node = i[0]
            if node not in graph:
                graph[node] = []
            vertices = list(set(graph[node] + i[1:]))
            graph[node] = vertices
    
    print("\nGraph Adjacency List --> ", graph)
    
    cargo_flights = list(graph.keys())
    airports = list(set([j for i in list(graph.values()) for j in i]))
    
    out_file = open('./output/outputPS15.txt', 'w')

    print("\nTotal number of cargo flights: ", len(cargo_flights))
    out_file.write("Total number of cargo flights: {}".format(len(cargo_flights)))
    
    print("Total number of Airports: ", len(airports))
    out_file.write("\nTotal number of Airports: {}".format(len(airports)))
    
    print("\nList of cargo flights: ")
    out_file.write("\n\nList of cargo flights: ")
    for i in cargo_flights:
        print(i)
        out_file.write("\n{}".format(i))

    print("\nList of Airports: ")
    out_file.write("\n\nList of Airports: ")
    for i in airports:
        print(i)
        out_file.write("\n{}".format(i))
    
    out_file.close()
    return graph

graph_data = readAirportFlightfile("./input/inputPS15.txt")

graph_adj_list = showAll(graph_data)


# In[ ]:




