
class Tile:

	def __init__(self,shade, elevate):
		"""
		Initialises the terrain tile and attributes
		"""
		self.shade=shade
		self.elevate=elevate

    # check if  tile is a slope
	def is_slope(self):
		if "," in self.elevate:
			return True
		return False

	def elevation(self):
		"""
		Returns an integer value of the elevation number
		of the terrain object
		"""
		# return the bigger number if it is a slope
		if "," in self.elevate:
			return int(self.elevate.split(",")[0])
		return int(self.elevate)

	def slope_elevation(self):
		if "," in self.elevate:
			return [int(i) for i in self.elevate.split(",")]


	def is_shaded(self):
		"""
		Returns True if the terrain tile is shaded, otherwise False
		"""
		if self.shade=="shaded":
			return True
		return False

	def set_occupant(self, obj):
		"""
		Sets the occupant on the terrain tile
		"""
		pass

	def get_occupant(self):
		"""
		Gets the entity on the terrain tile
		If nothing is on this tile, it should return None
		"""
		pass
