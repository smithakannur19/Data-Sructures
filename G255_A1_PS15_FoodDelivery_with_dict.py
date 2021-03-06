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
		self.adj_matrix, self.airports_dict, self.flights_dict = self.readAirportFlightfile(inputfile)
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


    # Operation 1:
	def readAirportFlightfile(self, inputfile):
		'''
    		This function reads the input file inputPS15.txt containing the name of the airport and the cargo flights between 
        	them in one line separated by a slash. 
        	A sample input file entry is shown below. 
        	The flight number is the first entry in each row followed by the different airports it services separated by a slash ???/???.
        	    indigo777 / Chennai / New Delhi
        	The function should create relevant vertices for both the cargo flights and its associated airports and relevant edges to 
        	indicate the association of a flight and its connecting airports. Ensure that the vertices are unique and there are no 
        	duplicates.
		'''
		try:
			with open(inputfile, "r") as f:
				data = f.readlines()
        		# print("Read Data --> ", data)

			airports_dict= {}
			flights_dict= {}
			graph_data = {}
			n_counter, e_counter = 0, 0
			for i in data:
				i = i.split("/")
				i = list(map(str.strip, i))
				if "" in i:
					i.remove("")
				if len(i) != 0:
					edge = i[0]
					nodes = i[1:]
					if edge not in graph_data:
						graph_data[edge] = []
						for n in nodes:
							if n not in graph_data[edge]:
								graph_data[edge].append(n)
					if edge not in list(flights_dict.keys()):
						flights_dict[edge] = e_counter
						e_counter = e_counter + 1
					for n in nodes:
						if n not in list(airports_dict.keys()):
							airports_dict[n] = n_counter
							n_counter = n_counter + 1
		
		    # Fill adjacency matrix
		    # matrix rows = flights
		    # matrix cols = airports    
			r,c = len(flights_dict), len(airports_dict)
			adj_matrix = [[0]*c for _ in range(r)]
		
		
			for flight in graph_data:
				row_id = flights_dict[flight]
				for airport in graph_data[flight]:
					col_id = airports_dict[airport]
					adj_matrix[row_id][col_id] = 1

			return adj_matrix, airports_dict, flights_dict        	
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
			cargo_flights = list(self.flights_dict.keys())
			airports = list(self.airports_dict.keys())
		    
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
			The function is triggered when the ???searchHubAirport??? tag is found in the file promptsPS15.txt file.
    	'''
		try:
			max_tot_flights = 0
			hub_airport = ""
			hub_flights_lst = []
			airports = list(self.airports_dict.keys())
			flights = list(self.flights_dict.keys())
			for airport in airports:
		        # print(self.airports_dict[airport])
				airport_id = self.airports_dict[airport]
		        # print(airport_id)
				total_flights = 0
				flights_lst = []
				for flight in flights:
					flight_id = self.flights_dict[flight]
					total_flights += self.adj_matrix[flight_id][airport_id]
					if self.adj_matrix[flight_id][airport_id]:
						flights_lst.append(flight)
				if max_tot_flights < total_flights:
					max_tot_flights = total_flights
					hub_airport = airport
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
			connected_airports = []
			airports = list(self.airports_dict.keys())
			flight_id = self.flights_dict[flight]
			for airport in airports:
				airport_id = self.airports_dict[airport]
				if self.adj_matrix[flight_id][airport_id]:
					connected_airports.append(airport)
		
		    
		
			output_msg = "\n--------Function displayConnectedAirports --------"
			output_msg += "\nCargo flight number: {}".format(flight)
			output_msg += "\nNumber of airports connected: {}".format(len(connected_airports))
			output_msg += "\nList of airports connected directly by : {}".format(flight)
			for ap in connected_airports:
				output_msg += "\n {}".format(ap)
			output_msg += "\n-----------------------------------------\n"
			if internal==False:
				print(output_msg)
				self.write_to_file(output_msg)
			return connected_airports
		except Exception as e:
			print(e)

    # Helper function: 3
	def displayConnectedFlights(self, airport):
		'''
    		This function displays all the flights that are connected to a single airport.	
		'''
		try:
			connected_flights = []
			flights = list(self.flights_dict.keys())
			airport_id = self.airports_dict[airport]
			for flight in flights:
				flight_id = self.flights_dict[flight]
				if self.adj_matrix[flight_id][airport_id]:
					connected_flights.append(flight)

		    

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
			flights = list(self.flights_dict.keys())
			airport_a_id, airport_b_id = self.airports_dict[airport_a], self.airports_dict[airport_b]
			for flight in flights:
				flight_id = self.flights_dict[flight]
				if self.adj_matrix[flight_id][airport_a_id] & self.adj_matrix[flight_id][airport_b_id]:
					output_msg += "Food box can be sent directly: Yes, {}\n".format(flight)
					output_msg += "-----------------------------------------\n"
					if internal==False:
						print(output_msg)
						self.write_to_file(output_msg)
					return flight
			output_msg += "Food box can be sent directly: No, There are no direct flights available.\n"
			output_msg += "-----------------------------------------\n"
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
			# self.visited_airports = [False]*len(self.airports_dict)
			# self.path = []

		    # Notice that case0 won't occur since if there is no path from a -> b then b won't be marked as visited
		    # # case0: No service available (all airports visited)
		    # if all(self.visited_airports):
		    #     print("No service available")
		    #     return -1

		    # Case1: Already visited source airport
			if self.visited_airports[self.airports_dict[airport_a]]:
				return None

		    # Case2: Destination airport found/ Direct flight exists to destination
			elif (flight := self.displayDirectFlight(airport_a, airport_b, True)) is not None:
				self.path.insert(0,airport_b)
				self.path.insert(0,flight)
				return True

		    # Case3: Destination airport not found / No direct flight exists to destination (Recursive calls)
			else:
		        # mark source airport as visited
				self.visited_airports[self.airports_dict[airport_a]] = True
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
			self.visited_airports = [False]*len(self.airports_dict)
			self.path = []
			output_msg = "\n--------Function findServiceAvailable --------\n"
			output_msg += "Airport A: {}\n".format(airport_a)
			output_msg += "Airport B: {}\n".format(airport_b)
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

