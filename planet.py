class Planet:
	def __init__(self, name, width, height):
		"""
		Initialise the planet object
		"""
		self.name=name
		self.width=int(width)
		self.height=int(height)
		self.tiles=[]
		self.dim=self.width*self.height

	# make tiels on the planet according to the dimension of the plapent
	def make_tiles(self,tiles):
		sub_lst=[]
		row=0
		beg_point=0
		end_point=self.width
		while row<self.height:
			for i in range(beg_point,end_point):
				sub_lst.append(tiles[i])

			self.tiles.append(sub_lst)
			sub_lst=[]
			beg_point=end_point
			end_point+=self.width
			row+=1
		return
