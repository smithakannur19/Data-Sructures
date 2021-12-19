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

# In[1]:


import os


# In[2]:


class foodDelivery(object):
    def __init__(self):
        self.visited_node = {}
        self.visited_edge = {}
        self.graph_data = {}
        
        self.path_to_outfile = "./output/outputPS15.txt"
        
    def visited_nodes_edges(self, data):
        try:
            n_counter, e_counter = 0, 0
            for i in data:
                # process the data
                i = i.split("/")
                i = list(map(str.strip, i))
                if "" in i:
                    i.remove("")
                if len(i) != 0:
                    edge = i[0]
                    nodes = i[1:]
                    if edge not in self.graph_data:
                        # graph_data is a dictionary with key as edge and values as node
                        self.graph_data[edge] = []
                        for n in nodes:
                            if n not in self.graph_data[edge]:
                                self.graph_data[edge].append(n)
                    if edge not in list(self.visited_edge.keys()):
                        # Collect unique edges
                        self.visited_edge[edge] = e_counter
                        e_counter = e_counter + 1
                    for n in nodes:
                        # Collect unique nodes
                        if n not in list(self.visited_node.keys()):
                            self.visited_node[n] = n_counter
                            n_counter = n_counter + 1
        except Exception as e:
            print(e)
    
    def get_key(self, dictionary, val):
        try:
            for key, value in dictionary.items():
                if val == value:
                    return key
        except Exception as e:
            print(e)
    
    # question 1
    def readAirportFlightfile(self, inputfile):
        """
        This function reads the input file inputPS15.txt containing the name of the airport and the cargo flights between 
        them in one line separated by a slash. 
        A sample input file entry is shown below. 
        The flight number is the first entry in each row followed by the different airports it services separated by a slash ‘/’.
            indigo777 / Chennai / New Delhi
        The function should create relevant vertices for both the cargo flights and its associated airports and relevant edges to 
        indicate the association of a flight and its connecting airports. Ensure that the vertices are unique and there are no 
        duplicates.
        """
        
        try:
            # read the input file
            if not os.path.exists(inputfile):
                print("Input file does not exists!!!")
                
            else:
                with open(inputfile, "r") as f:
                    data = f.readlines()
                #print("\nRead Data --> ", data)
            return data
        except Exception as e:
            print(e)
    
    # question 2
    def showAll(self):
        """
        This function displays the count of unique cargo flights and airports entered through the input file. 
        It should also list out the unique cargo flights and airports that have cargo service stored. 
        This function is called after all input data has been captured. 
        The output of this function should be pushed into outputPS15.txt file. 
        """
        try:
            # prepare adjaceny matrix
            node_size = len(self.visited_node)
            self.adj_matrix = [[0]*node_size for i in range(node_size)]

            for e in self.graph_data:
                edge = e
                node = self.graph_data[e]
                node_pairs = [[node[i], node[i + 1]] for i in range(len(node) - 1)]
                for pair in node_pairs:
                    n1 = pair[0]
                    n2 = pair[1]
                    n1_index, n2_index = self.visited_node[n1], self.visited_node[n2]
                    self.adj_matrix[n1_index][n2_index] = e
                    self.adj_matrix[n2_index][n1_index] = e

            print("Adjaceny Matrix = ")
            print(self.adj_matrix)

            cargo_flights = list(self.visited_edge.keys())
            airports = list(self.visited_node.keys())

    #         if not os.path.exists(self.path_to_outfile):
    #             print("Output file path {} does not exist.".format(self.path_to_outfile))
    #             out_file = open(self.path_to_outfile,"a+")

            out_file = open(self.path_to_outfile, 'a+')

            print("\n-------Function showAll --------")
            out_file.write("-------Function showAll --------")


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

            print("-"*50)
            out_file.write("-"*50)

            out_file.close()
        except Exception as e:
            print(e)
    
    # question 3
    def displayHubAirport(self, airport):
        """
        This function displays the name of the airport which is visited by the most number of cargo flights. 
        The function also displays the names of the incoming cargo flights to the outputPS15 file. 
        The function is triggered when the ‘searchHubAirport’ tag is found in the file promptsPS15.txt file. 
        """
        try:
            out_file = open(self.path_to_outfile, 'a+')

            print("\n---------Function displayHubAirport--------")
            out_file.write("---------Function displayHubAirport--------")

            flights = []
            row_ind = self.visited_node[airport]
            for col in self.adj_matrix[row_ind]:
                if col != 0:
                    flights.append(col)

            print("Main Hub Airport : {}".format(airport))
            out_file.write("Main Hub Airport : {}".format(airport))

            print("Number of Cargo flights visited : {}".format(len(flights)))
            out_file.write("Number of Cargo flights visited : {}".format(len(flights)))

            print("List of Cargo flights:")
            out_file.write("List of Cargo flights:")

            for i in flights:
                print(i)
                out_file.write(i)
        except Exception as e:
            print(e)
        
                
    # question 4
    def displayConnectedAirports(self, flight):
        """
        This function displays all the airports are connected by a single cargo flight. 
        """
        try:

            if flight in list(self.visited_edge.keys()):
                out_file = open(self.path_to_outfile, 'a+')

                print("\n--------Function displayConnectedAirports--------")
                out_file.write("--------Function displayConnectedAirports--------")

                print("Cargo flight number: {}".format(flight))
                out_file.write("Cargo flight number: {}".format(flight))

                airports = []
                for row in range(len(self.adj_matrix)):
                    for col in range(len(self.adj_matrix[row])):
                        if self.adj_matrix[row][col] == flight:
                            key1 = self.get_key(self.visited_node, row)
                            key2 = self.get_key(self.visited_node, col)
                            if key1 not in airports:
                                airports.append(key1)
                            if key2 not in airports:
                                airports.append(key2)

                print("Number of airports connected: {}".format(len(airports)))
                out_file.write("Number of airports connected: {}".format(len(airports)))

                print("List of airports connected directly by : {}".format(flight))
                out_file.write("List of airports connected directly by : {}".format(flight))

                for i in airports:
                    print(i)
                    out_file.write(i)

                print("-"*50)
                out_file.write("-"*50)

                out_file.close()
            else:
                print("{} not found!!!".format(flight))
        except Exception as e:
            print(e)

    # question 5
    def displayDirectFlight(self, airport_a, airport_b):
        """
        This function displays the cargo flight name which can be booked to send a food box directly from airport a to airport b. 

        """
        try:
            out_file = open(self.path_to_outfile, 'a+')

            print("\n---------Function displayDirectFlight--------")
            out_file.write("---------Function displayDirectFlight--------")

            row_index = self.visited_node[airport_a]
            col_index = self.visited_node[airport_b]
            if self.adj_matrix[row_index][col_index] == 0:
                print("Food box can be sent directly: No, as there is no direct flight from {} to {}".format(airport_a, airport_b))
                out_file.write("Food box can be sent directly: No, as there is no direct flight from {} to {}".format(airport_a, airport_b))
            else:
                print("Food box can be sent directly: Yes, {}".format(self.adj_matrix[row_index][col_index]))
                out_file.write("Food box can be sent directly: Yes, {}".format(self.adj_matrix[row_index][col_index]))

            print("-"*50)
            out_file.write("-"*50)

            out_file.close()
        except Exception as e:
            print(e)
    
    # question 6
    def findServiceAvailable(self, airport_a, airport_b):
        """
        This function finds whether a food box can be sent from airport a to airport b with any number of stops/transfers 
        (i.e. to deliver the food box from airport a to airport b it might even get transferred on another flight at an 
        intermediary airport c). 
        """
        try:
            out_file = open(self.path_to_outfile, 'a+')
            print("\n--------Function findServiceAvailable--------")
            out_file.write("--------Function findServiceAvailable--------")

            print("\nAirport A : {}".format(airport_a))
            out_file.write("\nAirport A : {}".format(airport_a))
            print("\nAirport B : {}".format(airport_b))
            out_file.write("\nAirport B : {}".format(airport_b))

            graph_nodes = {}
            for row in range(len(self.adj_matrix)):
                row_key = self.get_key(self.visited_node, row)
                graph_nodes[row_key] = []

                for col in range(len(self.adj_matrix[row])):
                    col_key = self.get_key(self.visited_node, col)
                    if (self.adj_matrix[row][col] != 0) and (self.adj_matrix[row][col] not in graph_nodes[row_key]):
                        graph_nodes[row_key] = [col_key]

            visited, queue, connected_nodes = [], [], []
            visited.append(airport_a)
            queue.append(airport_a)

            while queue:         
                m = queue.pop(0) 
                connected_nodes.append(m)

                for neighbour in graph_nodes[m]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)

            if airport_b in connected_nodes:
                ind = connected_nodes.index(airport_b)
                connected_nodes = connected_nodes[:ind]

                node_pairs = [[connected_nodes[i], connected_nodes[i + 1]] for i in range(len(connected_nodes) - 1)]
                result = []
                for i in node_pairs:
                    row, col = self.visited_node[i[0]], self.visited_node[i[1]]
                    edge = self.adj_matrix[row][col]
                    result.append(i[0]+">>"+edge+">>"+i[1])
                print("Can the food box be sent: Yes, {}".format(result))
                out_file.write("Can the food box be sent: Yes, {}".format(result))
            else:
                print("Can the food box be sent: No, there are no flight services available")
                out_file.write("Can the food box be sent: No, there are no flight services available")

            print("-"*50)
            out_file.write("-"*50)

            out_file.close()
        except Exception as e:
            print(e)
        


# In[3]:


obj = foodDelivery()

data = obj.readAirportFlightfile("./input/inputPS15.txt")
obj.visited_nodes_edges(data)
obj.showAll()

data = obj.readAirportFlightfile("./input/promptsPS15.txt")
for i in data:
    if "searchHubAirport" in i:
        airport = i.split(":")[-1].strip()
        obj.displayHubAirport(airport)
    elif "searchFlight" in i:
        flight = i.split(":")[-1].strip()
        obj.displayConnectedAirports(flight)
    elif "searchAirports" in i:
        airport_a = i.split(":")[1].strip()
        airport_b = i.split(":")[2].strip()
        obj.displayDirectFlight(airport_a, airport_b)
    elif "ServiceAvailability" in i:
        airport_a = i.split(":")[1].strip()
        airport_b = i.split(":")[2].strip()
        obj.findServiceAvailable(airport_a, airport_b)


# In[ ]:




