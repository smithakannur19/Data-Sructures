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


class foodDelivery(object):
	def __init__(self, inputfile, promptfile, outputfile):
		'''
			1. Read the input file with airports and flights details
			2. Show list of all airports and flights
			3. Reads the promp file and execute functions as given in it
		'''
		self.outputfile = outputfile
    	# Read input file with airports and flights details
		self.adj_matrix, self.airports_list, self.flights_list = self.readAirportFlightfile(inputfile)
		self.showAll()
		# self.print_matrix(self.adj_matrix)
    	# Read prompt file and execute instructions/functions
		self.readPromptFile(promptfile)

		

    # Helper function: 1
	def write_to_file(self, message):
		'''
    	This is the helper function that writes a given string into 
    	the output file "outputPS15.txt"
    	'''
		try:
			out_file = open(self.outputfile, 'a')
			out_file.write(message)
			out_file.close()
		except Exception as e:
			print(e)

    # Helper function: 2
	def print_matrix(self, matrix):
		'''
			Helper function to print the content of a given matrix
		'''
		try:
			r,c = len(matrix), len(matrix[0])
			for i in range(r):
				for j in range(c):
					print(matrix[i][j], end='\t')
				print()
		except Exception as e:
			print(e)

	# Helper function: 3
	def get_list_item_id(self, list_name, item_name):
		'''
			Return the index of the item in the given list
		'''
		try:
			return list_name.index(item_name)
		except ValueError as e:
			print(e)



    # Operation 1:
	def readAirportFlightfile(self, inputfile):
		'''
    		This function reads the input file inputPS15.txt containing the name of the airport and the cargo flights between 
        	them in one line separated by a slash. 
        	A sample input file entry is shown below. 
        	The flight number is the first entry in each row followed by the different airports it services separated by a slash ‘/’.
        	    indigo777 / Chennai / New Delhi
        	The function should create relevant vertices for both the cargo flights and its associated airports and relevant edges to 
        	indicate the association of a flight and its connecting airports. Ensure that the vertices are unique and there are no 
        	duplicates.
		'''
		try:
			with open(inputfile, "r") as f:
				data = f.readlines()
        		# print("Read Data --> ", data)

			# Contain the set of airports (index will be used as the id in adj_matrix)
			airports_list= []
			# Contain the set of flights (index will be used as the id in adj_matrix)
			flights_list= []
			# Contains list of airports connected with flight denoted by index
			graph_data = []

			# Handle data read, line by line
			for line in data:
				# Split the line with "/"
				line = line.split("/")
				line = list(map(str.strip, line))
				if "" in line:
					line.remove("")
				# if the line is not empty then process the line
				if len(line) != 0:
					# After splitting first item would be the flight name
					flight = line[0]
					# After rest of the list would be airport names
					connected_airports = line[1:]
					
					# Populate flights list while cheking for duplicates
					if flight not in flights_list:
						flights_list.append(flight)

					# Populate airports list while cheking for duplicates
					for n in connected_airports:
						if n not in airports_list:
							airports_list.append(n)

					# Get the flight id from the flight list using helper function
					flight_id = self.get_list_item_id(flights_list,flight)

					# populate the temporary nested list(graph_data) to store the graph data
					if flight_id < len(graph_data): # If the flight id already exists in graph_data
						for n in connected_airports: # then append airports to it one by one
							if n not in graph_data[flight_id]:
								graph_data[flight_id].append(n)
					else: # If the flight id doesn't exist in graph_data then assign the airports list to it
						graph_data.append(connected_airports)

					# print(graph_data)

		

			# Get the total count of flights and airports
			r,c = len(flights_list), len(airports_list)
			# Define and initialize the adjacency matrix
		    # matrix rows denotes flights
		    # matrix cols denotes airports			
			adj_matrix = [[0]*c for _ in range(r)]

		    # Fill adjacency matrix
			for flight_id in range(len(graph_data)):
				for airport in graph_data[flight_id]:
					airport_id = self.get_list_item_id(airports_list,airport)
					adj_matrix[flight_id][airport_id] = 1

			return adj_matrix, airports_list, flights_list        	
		except Exception as e:
			print(e)


    # Operation 2:
	def showAll(self):
		'''
			This function displays the count of unique cargo flights and airports 
			entered through the input file. It should also list out the unique cargo flights and airports that 
			have cargo service stored. This function is called after all input data has been captured. The 
			output of this function should be pushed into outputPS15.txt file. 
		'''
		try:
			cargo_flights = self.flights_list
			airports = self.airports_list
		    
			output_msg = "--------Function showAll --------\n"
		    
			output_msg += "Total number of cargo flights: {}\n".format(len(cargo_flights))
		    
			output_msg += "Total number of Airports: {}\n".format(len(airports))
		    
			output_msg += "\nList of cargo flights: "
			for i in cargo_flights:
				output_msg += "\n{}".format(i)

			output_msg += "\n\nList of Airports: "
			for i in airports:
				output_msg += "\n{}".format(i)
		    
			output_msg += "\n---------------------------------------\n"
			print(output_msg)
			self.write_to_file(output_msg)			
		except Exception as e:
			print(e)	


    # Operation 3:
	def displayHubAirport(self):
		'''
    		This function displays the name of the airport which is visited by the most number of cargo flights. 
    		The function also displays the names of the incoming cargo flights to the outputPS15 file. 
			The function is triggered when the ‘searchHubAirport’ tag is found in the file promptsPS15.txt file.
    	'''
		try:
			# Initialize the required variables
			max_tot_flights = 0
			hub_airport = ""
			hub_flights_lst = []

			# Iterate through all airports
			for airport_id in range(len(self.airports_list)):
				# Initialize total flights and flight list for each airport
				total_flights = 0
				flights_lst = []
				# Iterate through all flights 
				for flight_id in range(len(self.flights_list)):
					# Get the count of connected flights by adding the values in the related matrix column
					total_flights += self.adj_matrix[flight_id][airport_id]
					# Append the connected flights to the temporary flights list
					if self.adj_matrix[flight_id][airport_id]:
						flights_lst.append(self.flights_list[flight_id])
				# Check whether current max exceeds the previous max and update the values accordingly
				if max_tot_flights < total_flights:
					max_tot_flights = total_flights
					hub_airport = self.airports_list[airport_id]
					hub_flights_lst = flights_lst
		
		    
		
			output_msg = "\n\n--------Function displayHubAirport --------\n"
			output_msg += "Main hub airport: {}\n".format(hub_airport)
			output_msg += "Number of cargo flights visited: {}\n".format(max_tot_flights)
			output_msg += "List of Cargo Flights:\n"
			for f in hub_flights_lst:
				output_msg += "{}\n".format(f)
			output_msg += "-----------------------------------------\n"
			print(output_msg)
			self.write_to_file(output_msg)    		
		except Exception as e:
			print(e)	


	# Operation 4
	def displayConnectedAirports(self, flight, internal=False):
		'''
			This function displays all the airports are connected by a single cargo flight. 
			The function reads the input cargo flight number from the file promptsPS15.txt with the tag as shown below.
			searchFlight: Indigo666
			searchFlight: AirIndia111
			The output of this function should be appended into outputPS15.txt file. 
			If a flight is not found, an appropriate message should be output to file.
		'''
		try:
			# List to keep connected airports
			connected_airports = []
			# get id of the flight
			flight_id = self.get_list_item_id(self.flights_list,flight)

			# Check for connection for each airport
			for airport_id in range(len(self.airports_list)):
				if self.adj_matrix[flight_id][airport_id]:
					connected_airports.append(self.airports_list[airport_id])
		
		    
		
			output_msg = "\n--------Function displayConnectedAirports --------"
			output_msg += "\nCargo flight number: {}".format(flight)
			output_msg += "\nNumber of airports connected: {}".format(len(connected_airports))
			output_msg += "\nList of airports connected directly by : {}".format(flight)
			for ap in connected_airports:
				output_msg += "\n {}".format(ap)
			output_msg += "\n-----------------------------------------\n"
			# Below is to check whether this method is called directly or called by another method.
			# Only print and write to output file if called directly.
			if internal==False:
				print(output_msg)
				self.write_to_file(output_msg)
			return connected_airports
		except Exception as e:
			print(e)

    # Helper function: 4
	def displayConnectedFlights(self, airport):
		'''
    		This function displays all the flights that are connected to a single airport.	
		'''
		try:
			# List to keep connected flights
			connected_flights = []
			# Get the id of the airport
			airport_id = self.get_list_item_id(self.airports_list,airport)

			# Check for connection for each flight
			for flight_id in range(len(self.flights_list)):
				if self.adj_matrix[flight_id][airport_id]:
					connected_flights.append(self.flights_list[flight_id])

			output_msg = "\n--------Function displayConnectedFlights --------"
			output_msg += "\nAirport : {}".format(airport)
			output_msg += "\nNumber of flights connected: {}".format(len(connected_flights))
			output_msg += "\nList of flights connected directly to : {}".format(airport)
			for fl in connected_flights:
				output_msg += "\n {}".format(fl)
			output_msg += "\n-----------------------------------------\n"
		    # print(output_msg)
		    # self.write_to_file(output_msg)
			return connected_flights
		except Exception as e:
			print(e)


    # Operation: 5
	def displayDirectFlight(self, airport_a, airport_b, internal=False):
		'''
    		This function displays the cargo flight name which can be booked to send a food box directly from airport a to airport b.	
		'''
		try:
			output_msg = "\n--------Function displayDirectFlight --------\n"
			output_msg += "Airport A: {}\n".format(airport_a)
			output_msg += "Airport B: {}\n".format(airport_b)
			
			# Get indices of two airports
			airport_a_id = self.get_list_item_id(self.airports_list,airport_a)
			airport_b_id = self.get_list_item_id(self.airports_list,airport_b)
			
			# Check for connection for each flight
			for flight_id in range(len(self.flights_list)):
				# Both airports should be connected to the same flight for them to be connected
				if self.adj_matrix[flight_id][airport_a_id] & self.adj_matrix[flight_id][airport_b_id]:
					output_msg += "Food box can be sent directly: Yes, {}\n".format(self.flights_list[flight_id])
					output_msg += "-----------------------------------------\n"
					if internal==False:
						print(output_msg)
						self.write_to_file(output_msg)
					return self.flights_list[flight_id]

			# 
			output_msg += "Food box can be sent directly: No, There are no direct flights available.\n"
			output_msg += "-----------------------------------------\n"
			# Below is to check whether this method is called directly or called by another method.
			# Only print and write to output file if called directly.
			if internal==False:
				print(output_msg)
				self.write_to_file(output_msg)
			return None
		except Exception as e:
			print(e)


    # Operation: 6
	def findServiceAvailableRecursive(self, airport_a, airport_b):
		'''
    	This function finds whether a food box can be sent from airport a to airport b 
    	with any number of stops/transfers (i.e. to deliver the food box from airport a to airport b 
    	it might even get transferred on another flight at an intermediary airport c).

		Algorithm:
			1. check if direct flight is available by calling displayDirectFlight(self, airport a, airport b)
			2. If yes, then return the path and exit
			3. If No, get the list of connected flights of the source airport
    			4. For each flight get the list of connected air ports
        			5. Keep a record on the visited airports
        			6. Repeat recursively until direct flight to the destination airport is found

    	'''
		try:
		    # Notice that case0 won't occur since if there is no path from a -> b then b won't be marked as visited
		    # # case0: No service available (all airports visited)
		    # if all(self.visited_airports):
		    #     print("No service available")
		    #     return -1

		    # Case1: Already visited source airport
			if self.visited_airports[self.get_list_item_id(self.airports_list,airport_a)]:
				return None

		    # Case2: Destination airport found/ Direct flight exists to destination
			elif (flight := self.displayDirectFlight(airport_a, airport_b, True)) is not None:
				self.path.insert(0,airport_b)
				self.path.insert(0,flight)
				return True

		    # Case3: Destination airport not found / No direct flight exists to destination (Recursive calls)
			else:
		        # mark source airport as visited
				self.visited_airports[self.get_list_item_id(self.airports_list,airport_a)] = True
		        # List of connected flights to source airport
				connected_flights = self.displayConnectedFlights(airport_a)
				for connected_flight in connected_flights:
		            # List of connected airports for a connected flight
					connected_airports = self.displayConnectedAirports(connected_flight,True)
					for connected_airport in connected_airports:
		                # Recursively find the path from connected airport to destination airport
		                # print("Call -> findServiceAvailableRecursive({},{})".format(connected_airport,airport_b))
						result = self.findServiceAvailableRecursive(connected_airport,airport_b)
		                # print("Call -> findServiceAvailableRecursive({},{})  Result: {}".format(connected_airport,airport_b,result))
		                # Merge the result from recursive call
						if result==True:
							self.path.insert(0,connected_airport)
							self.path.insert(0,connected_flight)
							return result
		except Exception as e:
			print(e)


    # Wrapper function for findServiceAvailableRecursive()        
	def findServiceAvailable(self, airport_a, airport_b):
		try:
			# List variable to keep track of visited airports
			self.visited_airports = [False]*len(self.airports_list)
			# List variable to keep track of the path while traversing the graph
			self.path = []

			output_msg = "\n--------Function findServiceAvailable --------\n"
			output_msg += "Airport A: {}\n".format(airport_a)
			output_msg += "Airport B: {}\n".format(airport_b)

			# First call of the recursive function
			self.findServiceAvailableRecursive(airport_a,airport_b)
			if len(self.path)!=0:
		        # self.path.insert(0,airport_a)
				output_msg += "Can the food box be sent: Yes, "
				output_msg += "{} ".format(airport_a)
				for i in self.path:
					output_msg += "> {} ".format(i)
		    # This condition is not being hit. Check !!!
			else:
				output_msg += "Can the food box be sent: No, Sorry there is no service available from {} to {}\n".format(airport_a,airport_b)
			output_msg += "\n-----------------------------------------\n"
			print(output_msg)
			self.write_to_file(output_msg)
		except Exception as e:
			print(e)

    # Helper function: 4        
	def readPromptFile(self, promptfile):
		'''
    		Reads prompt file and execute functions accordingly.
    	'''
		try:
			with open(promptfile, "r") as f:
				data = f.readlines()
				# print("Prompt Data --> ", data)
			for i in data:
				if "searchHubAirport" in i:
					# airport = i.split(":")[-1].strip()
					self.displayHubAirport()
				elif "searchFlight" in i:
					flight = i.split(":")[-1].strip()
					self.displayConnectedAirports(flight)
				elif "searchAirports" in i:
					airport_a = i.split(":")[1].strip()
					airport_b = i.split(":")[2].strip()
					self.displayDirectFlight(airport_a, airport_b)
				elif "ServiceAvailability" in i:
					airport_a = i.split(":")[1].strip()
					airport_b = i.split(":")[2].strip()
					self.findServiceAvailable(airport_a, airport_b)
		except Exception as e:
			print(e)




if __name__ == "__main__":
	foodDelivery('inputPS15.txt', 'promptsPS15.txt', 'outputPS15.txt')

