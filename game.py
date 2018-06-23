import sys
import os
from planet import Planet
from loader import load_level
from rover import Rover
from terrain import Tile

def quit():
	"""
	Will quit the program
	"""
	return sys.exit()

def menu_help():
	"""
	Displays the help menu of the game
	"""
	help_msg= '''
START <level file> - Starts the game with a provided file.
QUIT - Quits the game
HELP - Shows this message
'''
	print(help_msg)
def menu_start_game(filepath):
	"""
	Will start the game with the given file path
	"""

	#make planet, tile, and rover objects
	pla=load_level(filepath)[0]
	til=load_level(filepath)[1]
	rov=load_level(filepath)[2]
	# produce tiels on planet
	pla.make_tiles(til)
	# user interation menu
	game_run=True
	while game_run:
		user_input=input()
		if user_input=="SCAN shade":
			scan_shade(pla,til,rov)
			rov.track_tiles(pla)
		elif user_input=="SCAN elevation":
			scan_elevation(pla,til,rov)
			rov.track_tiles(pla)
		if user_input.startswith("SCAN"):
			if "elevation" not in user_input and "shade" not in user_input:
				print("Cannot perform this command")
		elif user_input=="FINISH":
			rov.get_explored(pla)
			menu()
		elif user_input.startswith("MOVE"):
			direction = user_input[5]
			cycles= user_input[7:]
			move(pla,til,rov,direction,cycles)
		elif user_input=="STATS":
			print()
			print("Explored: {}%".format(int(rov.tile_explored/pla.dim*100)))
			print("Battery: {}/100".format(rov.battery))
			print()
		elif user_input.startswith("WAIT"):
			cycles=user_input[5:]
			if not pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_shaded():
				rov.add_battery(cycles)
				if rov.battery>100:
					rov.set_battery(100)
def level_file_format(filepath):
	#check if the data is structured properly
	format_check = True

	with open(filepath) as mf:
			if "name" not in mf.readlines()[1]:
				format_check=False

	with open(filepath) as mf:
		lines=mf.readlines()
		for i in range(len(lines)):
			if lines[i].startswith("height"):
				if int(lines[i][7:])<=0:
					format_check=False
					break



	return format_check
def menu():
	"""
	Start the menu component of the game
	"""


	game_run=True
	while game_run:
		user_input= input()

		if user_input=="QUIT":
			game_run=False
			quit()
		elif user_input=="HELP":
			menu_help()
		elif user_input.startswith("START"):
			check_path = user_input[6:]
			if os.path.exists(check_path):
				if level_file_format(check_path):
					menu_start_game(check_path)
				else:
					print()
					print("Unable to load level file")
					print()
			else:
				print()
				print("Level file could not be found")
				print()
		else:
			print()
			print("No menu item")
			print()

def scan_shade(pla,til,rov):
	# produce tiels on planet
	#pla=load_level("first.level")[0]
	#til=load_level("first.level")[1]
	#pla.make_tiles(til)
	# get rover initial position
	rov_x_pos=rov.get_pos_x()
	rov_y_pos=rov.get_pos_y()
	# get topleft and bottom right position of tiles
	beg_x_pos= rov_x_pos-2
	beg_y_pos= rov_y_pos-2
	end_x_pos= rov_x_pos+2
	end_y_pos= rov_y_pos+2
	#get current postion of scaning
	cur_x=beg_x_pos
	cur_y=beg_y_pos
	row=0
	col=0
	print("")
	while row<5:
		while col<5:

			if col==row==2:
				print("|H",end="")  # H at the centre

			#wraping aroud the planet
			if cur_x<0 or cur_x>=pla.width:
				out_x=int(cur_x%pla.width)
			else:
				out_x=cur_x
			if cur_y<0 or cur_y>=pla.height:
				out_y=int(cur_y%pla.height)
			else:
				out_y=cur_y


			if pla.tiles[out_y][out_x].is_shaded() and not col==row==2:
				print("|#",end="")
			if not pla.tiles[out_y][out_x].is_shaded() and not col==row==2:
				print("| ",end="")
			cur_x+=1
			col+=1

		print("|")
		cur_y+=1
		cur_x=beg_x_pos
		col=0
		row+=1
	print()
def scan_elevation(pla,til,rov):
	# produce tiels on planet
	#pla=load_level("first.level")[0]
	#til=load_level("first.level")[1]
	#pla.make_tiles(til)
	# get rover initial position
	rov_x_pos=rov.get_pos_x()
	rov_y_pos=rov.get_pos_y()
	# get topleft and bottom right position of tiles
	beg_x_pos= rov_x_pos-2
	beg_y_pos= rov_y_pos-2
	end_x_pos= rov_x_pos+2
	end_y_pos= rov_y_pos+2
	#get current postion of scaning
	cur_x=beg_x_pos
	cur_y=beg_y_pos
	row=0
	col=0
	print()
	#Cases where rover is not on a slope
	if not pla.tiles[rov_y_pos][rov_x_pos].is_slope():
		rov_elv=int(pla.tiles[rov_y_pos][rov_x_pos].elevation())

		while row<5:
			while col<5:
				if col==row==2:
					print("|H",end="")

				#wraping aroud the planet
				if cur_x<0 or cur_x>=pla.width:
					out_x=int(cur_x%pla.width)
				else:
					out_x=cur_x
				if cur_y<0 or cur_y>=pla.height:
					out_y=int(cur_y%pla.height)
				else:
					out_y=cur_y

				# compare with slope tiles
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()==rov_elv:
					print("|\\",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()==rov_elv+1:
					print("|/",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()-1>rov_elv:
					print("|+",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()<rov_elv:
					print("|-",end="")
				# compare with non-slope tiles
				if not col==row==2 and pla.tiles[out_y][out_x].elevation()==rov_elv and pla.tiles[out_y][out_x].is_slope()==False:
					print("| ",end="")

				if not col==row==2 and pla.tiles[out_y][out_x].elevation()>rov_elv and pla.tiles[out_y][out_x].is_slope()==False:
					print("|+",end="")

				if not col==row==2 and pla.tiles[out_y][out_x].elevation()<rov_elv and pla.tiles[out_y][out_x].is_slope()==False:
					print("|-",end="")
				cur_x+=1
				col+=1

			print("|")
			cur_y+=1
			cur_x=beg_x_pos
			col=0
			row+=1
	# case where rover is on a slope
	if pla.tiles[rov_y_pos][rov_x_pos].is_slope():
		up_elv=int(pla.tiles[rov_y_pos][rov_x_pos].slope_elevation()[0])
		lo_elv=int(pla.tiles[rov_y_pos][rov_x_pos].slope_elevation()[1])

		while row<5:
			while col<5:
				if col==row==2:
					print("|H",end="")

				#wraping aroud the planet
				if cur_x<0 or cur_x>=pla.width:
					out_x=int(cur_x%pla.width)
				else:
					out_x=cur_x
				if cur_y<0 or cur_y>=pla.height:
					out_y=int(cur_y%pla.height)
				else:
					out_y=cur_y

				# compare with slope tiles
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()==up_elv+1:
					print("|/",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()==lo_elv:
					print("|\\",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()==up_elv:
					print("| ",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()<lo_elv:
					print("|-",end="")
				if pla.tiles[out_y][out_x].is_slope() and not col==row==2 and pla.tiles[out_y][out_x].elevation()-1>up_elv:
					print("|+",end="")
				# compare with non-slope tiles
				if not col==row==2 and ( pla.tiles[out_y][out_x].elevation()==up_elv or pla.tiles[out_y][out_x].elevation() ==lo_elv )and pla.tiles[out_y][out_x].is_slope()==False:
					print("| ",end="")

				if not col==row==2 and pla.tiles[out_y][out_x].elevation()>up_elv and not pla.tiles[out_y][out_x].is_slope():
					print("|+",end="")

				if not col==row==2 and pla.tiles[out_y][out_x].elevation()<lo_elv and not pla.tiles[out_y][out_x].is_slope():
					print("|-",end="")
				cur_x+=1
				col+=1

			print("|")
			cur_y+=1
			col=0
			row+=1
	print()
def move(pla,til,rov,direction,cycles):
	#North
	if direction=="N":

		cur_cyc=0
		end_cyc=int(cycles)
		next_pos=rov.get_pos_y()
		while cur_cyc<end_cyc:
			if next_pos-1<0:
				next_pos=(next_pos-1)%pla.height
			else:
				next_pos-=1

			# case where rover is not on a slope
			if not pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():

				if pla.tiles[next_pos][rov.get_pos_x()].elevation()!=pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and not pla.tiles[next_pos][rov.get_pos_x()].is_slope():
					next_pos+=1

					break
				if pla.tiles[next_pos][rov.get_pos_x()].is_slope() and (pla.tiles[next_pos][rov.get_pos_x()].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and pla.tiles[next_pos][rov.get_pos_x()].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation()+1):

					next_pos+=1

					break

			# case where rover is on a slope
			if pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():
				if not pla.tiles[next_pos][rov.get_pos_x()].is_slope() and pla.tiles[next_pos][rov.get_pos_x()].elevation() > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[next_pos][rov.get_pos_x()].elevation() < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
					next_pos+=1
					break
				if pla.tiles[next_pos][rov.get_pos_x()].is_slope():
					if pla.tiles[next_pos][rov.get_pos_x()].slope_elevation()[1] > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[next_pos][rov.get_pos_x()].slope_elevation()[0] < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
						next_pos+=1
						break

			# case where rover ran out of power
			if rov.see_battery()==0 and pla.tiles[next_pos][rov.get_pos_x()].is_shaded():
				next_pos+=1
				break

			rov.change_y(next_pos)
			if pla.tiles[next_pos][rov.get_pos_x()].is_shaded():
				rov.lose_battery()
			#move is count as explore
			lst=[rov.get_pos_x(),next_pos]

			if lst not in rov.explore_lst:

				rov.add_explore(lst)
			cur_cyc+=1
	# South
	if direction=="S":
		cur_cyc=0
		end_cyc=int(cycles)
		next_pos=rov.get_pos_y()
		while cur_cyc<end_cyc:
			if next_pos+1>=pla.height:
				next_pos=(next_pos+1)%pla.height
			else:
				next_pos+=1

			# case where rover is not on a slope
			if not pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():

				if pla.tiles[next_pos][rov.get_pos_x()].elevation()!=pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and not pla.tiles[next_pos][rov.get_pos_x()].is_slope():
					next_pos-=1

					break
				if pla.tiles[next_pos][rov.get_pos_x()].is_slope() and (pla.tiles[next_pos][rov.get_pos_x()].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and pla.tiles[next_pos][rov.get_pos_x()].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation()+1):

					next_pos-=1

					break

			# case where rover is on a slope
			if pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():
				if not pla.tiles[next_pos][rov.get_pos_x()].is_slope() and pla.tiles[next_pos][rov.get_pos_x()].elevation() > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[next_pos][rov.get_pos_x()].elevation() < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
					next_pos-=1
					break
				if pla.tiles[next_pos][rov.get_pos_x()].is_slope():
					if pla.tiles[next_pos][rov.get_pos_x()].slope_elevation()[1] > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[next_pos][rov.get_pos_x()].slope_elevation()[0] < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
						next_pos-=1
						break

			# case where rover ran out of power
			if rov.see_battery()==0 and pla.tiles[next_pos][rov.get_pos_x()].is_shaded():
				next_pos-=1
				break

			rov.change_y(next_pos)
			if pla.tiles[next_pos][rov.get_pos_x()].is_shaded():
				rov.lose_battery()
			#move is count as explore
			lst=[rov.get_pos_x(),next_pos]
			if lst not in rov.explore_lst:
				rov.add_explore(lst)
			cur_cyc+=1
	#West
	if direction=="W":
		cur_cyc=0
		end_cyc=int(cycles)
		next_pos=rov.get_pos_x()
		while cur_cyc<end_cyc:
			if next_pos-1<0:
				next_pos=(next_pos-1)%pla.width
			else:
				next_pos-=1

			# case where rover is not on a slope
			if not pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():

				if pla.tiles[rov.get_pos_y()][next_pos].elevation()!=pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and not pla.tiles[rov.get_pos_y()][next_pos].is_slope():
					next_pos+=1

					break
				if pla.tiles[rov.get_pos_y()][next_pos].is_slope() and (pla.tiles[rov.get_pos_y()][next_pos].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and pla.tiles[rov.get_pos_y()][next_pos].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation()+1):

					next_pos+=1

					break

			# case where rover is on a slope
			if pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():
				if not pla.tiles[rov.get_pos_y()][next_pos].is_slope() and pla.tiles[rov.get_pos_y()][next_pos].elevation() > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[rov.get_pos_y()][next_pos].elevation() < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
					next_pos+=1
					break
				if pla.tiles[rov.get_pos_y()][next_pos].is_slope():
					if pla.tiles[rov.get_pos_y()][next_pos].slope_elevation()[1] > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[rov.get_pos_y()][next_pos].slope_elevation()[0] < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
						next_pos+=1
						break

			# case where rover ran out of power
			if rov.see_battery()==0 and pla.tiles[rov.get_pos_y()][next_pos].is_shaded():
				next_pos+=1
				break

			rov.change_x(next_pos)
			if pla.tiles[rov.get_pos_y()][next_pos].is_shaded():
				rov.lose_battery()
			#move is count as explore
			lst=[next_pos,rov.get_pos_y()]
			if lst not in rov.explore_lst:
				rov.add_explore(lst)
			cur_cyc+=1
	#East
	if direction=="E":
		cur_cyc=0
		end_cyc=int(cycles)
		next_pos=rov.get_pos_x()
		while cur_cyc<end_cyc:
			if next_pos+1>=pla.width:
				next_pos=(next_pos+1)%pla.width
			else:
				next_pos+=1

			# case where rover is not on a slope
			if not pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():

				if pla.tiles[rov.get_pos_y()][next_pos].elevation()!=pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and not pla.tiles[rov.get_pos_y()][next_pos].is_slope():
					next_pos-=1

					break
				if pla.tiles[rov.get_pos_y()][next_pos].is_slope() and (pla.tiles[rov.get_pos_y()][next_pos].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation() and pla.tiles[rov.get_pos_y()][next_pos].elevation() != pla.tiles[rov.get_pos_y()][rov.get_pos_x()].elevation()+1):

					next_pos-=1

					break

			# case where rover is on a slope
			if pla.tiles[rov.get_pos_y()][rov.get_pos_x()].is_slope():
				if not pla.tiles[rov.get_pos_y()][next_pos].is_slope() and pla.tiles[rov.get_pos_y()][next_pos].elevation() > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[rov.get_pos_y()][next_pos].elevation() < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
					next_pos-=1
					break
				if pla.tiles[rov.get_pos_y()][next_pos].is_slope():
					if pla.tiles[rov.get_pos_y()][next_pos].slope_elevation()[1] > pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[0] or pla.tiles[rov.get_pos_y()][next_pos].slope_elevation()[0] < pla.tiles[rov.get_pos_y()][rov.get_pos_x()].slope_elevation()[1]:
						next_pos-=1
						break

			# case where rover ran out of power
			if rov.see_battery()==0 and pla.tiles[rov.get_pos_y()][next_pos].is_shaded():
				next_pos-=1
				break

			rov.change_x(next_pos)
			if pla.tiles[rov.get_pos_y()][next_pos].is_shaded():
				rov.lose_battery()
			#move is count as explore
			lst=[next_pos,rov.get_pos_y()]
			if lst not in rov.explore_lst:
				rov.add_explore(lst)
			cur_cyc+=1
menu()
