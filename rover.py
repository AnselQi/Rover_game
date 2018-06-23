
class Rover:

	def __init__(self,start_pos_x,start_pos_y ):
		"""
		Initialises the rover
		"""
		self.start_pos_x=int(start_pos_x)
		self.start_pos_y=int(start_pos_y)
		self.battery=100
		self.tile_explored=1
		self.explore_lst=[[self.start_pos_x,self.start_pos_y]]
	def get_pos_x(self):
		return int(self.start_pos_x)

	def get_pos_y(self):
		return int(self.start_pos_y)

	def move(self, direction, cycles):
		"""
		Moves the rover on the planet
		"""
		pass

	def wait(self, cycles):
		"""
		The rover will wait for the specified cycles
		"""
		pass

	def see_battery(self):
		return self.battery

	def set_battery(self,num):
		self.battery=num
	def add_battery(self,cycles):
		self.battery+=int(cycles)

	def lose_battery(self):
		self.battery-=1

	def rover_move(self,direction,cycles,width,height):
		if direction =="N":
			if self.start_pos_y-cycles <0:
				self.start_pos_y= (self.start_pos_y-cycles)%height
			else:
				self.start_pos_y=self.start_pos_y-cycles
		if direction=="S":
			if self.start_pos_y+cycles >=height:
				self.start_pos_y=(self.start_pos_y+cycles)%height
			else:
				self.start_pos_y=self.start_pos_y+cycles
		if direction=="W":
			if self.start_pos_x-cycles <0:
				self.start_pos_x= (self.start_pos_x-cycles)%width
			else:
				self.start_pos_x= self.start_pos_x-cycles
		if direction=="E":
			if self.start_pos_x+cycles >=width:
				self.start_pos_x=(self.start_pos_x+cycles)%width
			else:
				self.start_pos_x=self.start_pos_x+cycles
	# Finish command
	def get_explored(self,planet):
		print()
		print("You explored {}% of {}".format(int(self.tile_explored/planet.dim*100),planet.name))
		print()
		return
	def track_tiles(self,pla):
		# list explored tiles position
		row=0
		col=0
		start_x=self.get_pos_x()-2
		start_y=self.get_pos_y()-2
		while row<5:
			col=0
			while col<5:

				lst=[start_x+col,start_y+row]
				if lst[0]<0 or lst[0]>=pla.width:
					lst[0]=lst[0]%pla.width
				if lst[1]<0 or lst[1]>=pla.height:
					lst[1]=lst[1]%pla.height
				if lst not in self.explore_lst:
					self.explore_lst.append(lst)
				col+=1

			row+=1

		self.tile_explored=len(self.explore_lst)

	def change_x(self,new_x):
		self.start_pos_x=new_x
	def change_y(self,new_y):
		self.start_pos_y=new_y


	def add_explore(self,pos):
		self.explore_lst.append(pos)
		self.tile_explored=len(self.explore_lst)
