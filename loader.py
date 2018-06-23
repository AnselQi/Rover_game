from planet import Planet
from rover import Rover
from terrain import Tile
def load_level(filename):
	"""
	Loads the level and returns an object of your choosing
	"""
	# read data from level file
	with open(filename) as mf:
		planet_atr=[0]*4
		for line in mf:
			if line.startswith("name,"):
				planet_atr[0]=line[5:].rstrip()
			if line.startswith("width,"):
				planet_atr[1]=line[6:].rstrip()
			if line.startswith("height,"):
				planet_atr[2]=line[7:].rstrip()
			if line.startswith("rover,"):
				planet_atr[3]=line[6:].rstrip()
		dim= int(planet_atr[1])*int(planet_atr[2])
		#create planet obj
		planet=Planet(planet_atr[0],planet_atr[1],planet_atr[2])
		rov_pos=[x.strip() for x in planet_atr[3].split(',')]
		#create rover obj
		rover=Rover(rov_pos[0],rov_pos[1])

	## read tiles
	with open(filename) as mf:
		count=0
		for x,line in enumerate(mf):
			if line.startswith("[tiles]"):
				count=x
	with open(filename) as mf:
		tile_lst=mf.readlines()[count+1:count+dim+2]
		tile_lst=[i.rstrip() for i in tile_lst]
	tl_lst=[]
	for i in range(len(tile_lst)):
		shd=tile_lst[i][:6]
		ele=tile_lst[i][7:]
		tile=Tile(shd,ele)
		tl_lst.append(tile)
	## Compose planet, tiles and rover into a list
	red_lst=[planet,tl_lst,rover]

	return red_lst
