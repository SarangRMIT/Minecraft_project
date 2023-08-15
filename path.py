from mcpi import minecraft
from mcpi import block
import random

mc = minecraft.Minecraft.create()

# nested list of points where paths end
# each element of the list has x,y,z coordinated and direction it was built in (dirx or dirz)
global end_points
end_points = []

# offset values from the main path for the subpath to start
global sub_offset
sub_offset = []

global middle_points
middle_points = []

#storing id because its not part of the block class
grass_path_id = 208
# Function to find actual height of ground level (not on top of trees etc)
def getGroundHeight(x,y,z):
    # types of blocks that the road shouldn't be built on
    nonGroundBlocks = [block.WATER.id, block.AIR.id, block.LEAVES.id, block.WOOD.id, block.SAPLING.id]

    # current block type
    height = mc.getHeight(x,z)
    blocktype = mc.getBlockWithData(x,height,z)
    # print(blocktype)
    while blocktype.id in nonGroundBlocks:
            x += 1
            height = mc.getHeight(x,z)
            blocktype = mc.getBlockWithData(x,height,z)
    
    return x,height,z

# function to randomly generate directions in the x axis
def direction_z(z):
    #randomly generates direction
    direction = random.randint(0,1)

    if direction == 0:
        #north
        z += 1
        return 0, z

    else:
        #south
        z -= 1
        return 1, z

# function to randomly generate directions in the z axis
def direction_x(x):
    direction = random.randint(0,1)

    if direction == 0:
        #west
        return 0, (x + 1)
    
    else:
        return 1, (x - 1)

# function to check if there are trees where the path is building
def checkTree(x,y,z):
    #invalid block ids
    log_ids = 17
    leaf_ids = 18
    mushroom_block_id = 100
    mushroom_stem_id = 99
    cactus_id = 81
    #getting block data of current block and 30 above it because trees are tall
    block_ids = mc.getBlocks(x, y, z, x, y + 30, z)
    
    #if any of the blocks are logs or leaves, return true
    for i in block_ids:
        if i == log_ids or i == leaf_ids or i == mushroom_block_id or i == mushroom_stem_id or i == cactus_id:
            print('check tree is true')
            return True
        
    return False

# function to remove trees from the path
def removeTree(direction, x,y,z):
    new_x = x 
    new_z = z
    #finds height of tree
    new_y = mc.getHeight(x,z)

    # goes in direction of path and checks if block is a log (width of tree)
    if direction == 'posx':
        new_x += 5
        new_z += 5
    elif direction == 'negx':
        new_x -= 5
        new_z -= 5

    if direction == 'posz':
        new_z += 5
        new_x += 5

    elif direction == 'negz':
        new_z -= 5
        new_x -= 5

    #setting air blocks to remove tree
    mc.setBlocks(new_x, new_y, new_z, x, y, z, block.AIR.id)
    print('tree removed')

# make paths according to randomly generated starting points
def path_posx(x, y, z, path_length):
    for l in range(path_length):
        #storing the middle point of the path so lamposts can be added to it
        halfway = path_length // 2
        if l == halfway:
            middle_points.append([x,y,z])
        #checking if there is a tree in the way
        if checkTree(x,y,z):
            #removing tree
            removeTree('posx', x,y,z)
        # checking if block above is air and block below is not air
        if (mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x,y+1,z+1).id == block.AIR.id) and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x,y-1,z+1).id != block.AIR.id):
            #setting air blocks before the grass ensures the path is flush with the ground
            #also gets rid of potential tree remnants
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z+1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z+1, grass_path_id)
        
        else:
            old_y = y
            #finds nearest valid ground block
            y = mc.getHeight(x, z)
            
            #builds path, incrementing by 1 until it reaches a valid ground block
            while old_y != y:
                mc.setBlock(x, y, z, block.AIR.id)
                mc.setBlock(x, y, z+1, block.AIR.id)
                mc.setBlock(x, old_y, z, grass_path_id)
                mc.setBlock(x, old_y, z+1, grass_path_id)
                if old_y < y:
                    old_y += 1
                else:
                    old_y -= 1
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z + 1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z + 1, grass_path_id)
        x += 1
        #ensuring path doesn't stop in the middle of water
        l = 0
        while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z + 1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z + 1, grass_path_id)
            x  += 1
            l += 1

    #storing the end point of the path along with direction
    #this is used to build subpaths
    #the coordinates will also dictate where the house is built
    end_points.append([x,y,z, 'posx'])
    # returning end of path coordinates to use in the join_paths function
    return x,y,z


# the code in the rest of the path laying functions is essentially the same
# the only difference is the direction the path is built in
def path_negx(x, y, z, path_length):
    for l in range(path_length):
        halfway = path_length // 2
        if l == halfway:
            middle_points.append([x,y,z])
        if checkTree(x,y,z):
            removeTree('negx', x,y,z)
        # checking if block above is air and block below is not air
        if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x,y+1,z+1).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x,y-1,z+1).id != block.AIR.id):
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z+1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z+1, grass_path_id)
        else:
            old_y = y
            y = mc.getHeight(x, z)
            # print(old_y, y)
            while old_y != y:
                mc.setBlock(x, y, z, block.AIR.id)
                mc.setBlock(x, y, z+1, block.AIR.id)
                mc.setBlock(x, old_y, z, grass_path_id)
                mc.setBlock(x, old_y, z+1, grass_path_id)
                if old_y < y:
                    old_y += 1
                else:
                    old_y -= 1
            
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z + 1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z+1, grass_path_id)
        x -= 1
        l = 0
        while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x, y, z + 1, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x, y, z + 1, grass_path_id)
            x  -= 1
            l += 1
    end_points.append([x,y,z, 'negx'])
    return x,y,z

def path_posz(x, y, z, path_length):
    for l in range(path_length):
        halfway = path_length // 2
        if l == halfway:
            middle_points.append([x,y,z])
        if checkTree(x,y,z):
            removeTree('posz', x,y,z)
        # checking if block above is air and block below is not air
        if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x+1,y+1,z).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x+1,y-1,z).id != block.AIR.id):
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x + 1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x+1, y, z, grass_path_id)
        else:
            old_y = y
            y = mc.getHeight(x, z)
            # print(old_y, y)
           
            while old_y != y:
                mc.setBlock(x, y, z, block.AIR.id)
                mc.setBlock(x+1, y, z, block.AIR.id)
                mc.setBlock(x, old_y, z, grass_path_id)
                mc.setBlock(x+1, old_y, z, grass_path_id)
                if old_y < y:
                    old_y += 1
                else:
                    old_y -= 1

            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x+1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x+1, y, z, grass_path_id)
        z += 1
        l = 0
        while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x+1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x+1, y, z, grass_path_id)
            z  += 1
            l += 1
    end_points.append([x,y,z, 'posz'])
    return x,y,z

def path_negz(x, y, z, path_length):
    for l in range(path_length):
        halfway = path_length // 2
        if l == halfway:
            middle_points.append([x,y,z])
        if checkTree(x,y,z):
            removeTree('negz', x,y,z)
        # checking if block above is air and block below is not air
        if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x+1,y+1,z).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x+1,y-1,z).id != block.AIR.id):
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x + 1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x + 1, y, z, grass_path_id)
        else:
            old_y = y
            y = mc.getHeight(x, z)
            # print(old_y, y)

            while old_y != y:
                mc.setBlock(x, y, z, block.AIR.id)
                mc.setBlock(x + 1, y, z, block.AIR.id)
                mc.setBlock(x, old_y, z, grass_path_id)
                mc.setBlock(x + 1, old_y, z, grass_path_id)
                if old_y < y:
                    old_y += 1
                else:
                    old_y -= 1
  
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x+1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x+1, y, z, grass_path_id)
        z -= 1
        l = 0
        while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
            mc.setBlock(x, y, z, block.AIR.id)
            mc.setBlock(x + 1, y, z, block.AIR.id)
            mc.setBlock(x, y, z, grass_path_id)
            mc.setBlock(x + 1, y, z, grass_path_id)
            z  -= 1
            l += 1
    end_points.append([x,y,z, 'negz'])
    return x,y,z


# functions to make a subpath out of the main paths generated from the center points
# subpath along x axis
def subpath_x(center, x, y, z):
    # generate a random offset in the main path for the subpath to start
    offset = random.randrange(5, 10)

    sub_offset.append(offset)

    if z > center:
        z -= offset
        y = mc.getHeight(x, z)
    else:
        z += offset
        y = mc.getHeight(x, z)

    print('offsetx', offset)

    path_length = random.randint(45,55)
    print('subpath length:', path_length)

    dir, x = direction_x(x)

    for l in range(1, path_length):
            if dir == 0:
                #checking for trees and removing them
                if checkTree(x,y,z):
                    removeTree('posx', x,y,z)
                # checking if block above is air and block below is not air
                if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x,y+1,z+1).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x,y-1,z+1).id != block.AIR.id):
                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x, y, z+1, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x, y, z+1, grass_path_id)
                else:
                    # if it is air making it go up or down forming steps
                    old_y = y
                    y = mc.getHeight(x, z)
                    # print(old_y, y)
                   
                    # if it is air making it go up or down forming steps
                    while old_y != y:
                        mc.setBlock(x, y, z, block.AIR.id)
                        mc.setBlock(x, y, z+1, block.AIR.id)
                        mc.setBlock(x, old_y, z, grass_path_id)
                        mc.setBlock(x, old_y, z+1, grass_path_id)
                        if old_y < y:
                            old_y += 1
                        else:
                            old_y -= 1
                    
                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x, y, z + 1, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x, y, z+1, grass_path_id)
                x += 1
                continue
            else:
                #checking for trees and removing them
                if checkTree(x,y,z):
                    removeTree('negx', x,y,z)
                # checking if block above is air and block below is not air
                if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x,y+1,z+1).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x,y-1,z+1).id != block.AIR.id):
                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x, y, z+1, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x, y, z+1, grass_path_id)
                else:
                    old_y = y
                    y = mc.getHeight(x, z)
                    # print(old_y, y)

                    while old_y != y:
                        mc.setBlock(x, y, z, block.AIR.id)
                        mc.setBlock(x, y, z+1, block.AIR.id)
                        mc.setBlock(x, old_y, z, grass_path_id)
                        mc.setBlock(x, old_y, z+1, grass_path_id)
                        if old_y < y:
                            old_y += 1
                        else:
                            old_y -= 1

                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x, y, z + 1, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x, y, z+1, grass_path_id)
                
                x -= 1
    l = 0
    while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
        mc.setBlock(x, y, z, block.AIR.id)
        mc.setBlock(x, y, z + 1, block.AIR.id)
        mc.setBlock(x, y, z, grass_path_id)
        mc.setBlock(x, y, z + 1, grass_path_id)
        x -= 1
        l += 1
    if dir == 0:
        end_points.append([x,y,z, 'posx'])
    else:
        end_points.append([x,y,z, 'negx'])

#  subpath along z axis
def subpath_z(center, x, y, z):
    # generate a random offset in the main path for the subpath to start
    offset = random.randrange(5, 10)

    sub_offset.append(offset)


    if x > center:
        x -= offset
        y = mc.getHeight(x, z)
    else:
        x += offset
        y = mc.getHeight(x, z)
    print('offsetz', offset)

    path_length = random.randint(45,55)
    print('subpath length:', path_length)

    dir, z = direction_x(z)

    for l in range(1, path_length):
            if dir == 0:
                if checkTree(x,y,z):
                    removeTree('posz', x,y,z)
                # checking if block above is air and block below is not air
                if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x+1,y+1,z).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x+1,y-1,z).id != block.AIR.id):
                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x+1, y, z, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x+1, y, z, grass_path_id)

                else:
                    # if it is air making it go up or down forming steps
                    old_y = y
                    y = mc.getHeight(x, z)
                    # print(old_y, y)

                    while old_y != y:
                        mc.setBlock(x, y, z, block.AIR.id)
                        mc.setBlock(x+1, y, z, block.AIR.id)
                        mc.setBlock(x, old_y, z, grass_path_id)
                        mc.setBlock(x+1, old_y, z, grass_path_id)
                        if old_y < y:
                            old_y += 1
                        else:
                            old_y -= 1

                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x+1, y, z, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x+1, y, z, grass_path_id)
                z += 1
                continue
            
            else:
                if checkTree(x,y,z):
                    removeTree('negz', x,y,z)
                # checking if block above is air and block below is not air
                if mc.getBlockWithData(x,y+1,z).id == block.AIR.id and mc.getBlockWithData(x+1,y+1,z).id == block.AIR.id and (mc.getBlockWithData(x,y-1,z).id != block.AIR.id and mc.getBlockWithData(x+1,y-1,z).id != block.AIR.id):
                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x+1, y, z, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x+1, y, z, grass_path_id)

                else:
                    # if it is air making it go up or down forming steps
                    old_y = y
                    y = mc.getHeight(x, z)
                    # print(old_y, y)

                    while old_y != y:
                        mc.setBlock(x, y, z, block.AIR.id)
                        mc.setBlock(x+1, y, z, block.AIR.id)
                        mc.setBlock(x, old_y, z, grass_path_id)
                        mc.setBlock(x+1, old_y, z, grass_path_id)
                        if old_y < y:
                            old_y += 1
                        else:
                            old_y -= 1

                    mc.setBlock(x, y, z, block.AIR.id)
                    mc.setBlock(x+1, y, z, block.AIR.id)
                    mc.setBlock(x, y, z, grass_path_id)
                    mc.setBlock(x+1, y, z, grass_path_id)
                
                z -= 1
                continue
    l = 0
    while mc.getBlock(x,y,z) == block.WATER.id and l < 7:
        mc.setBlock(x, y, z, block.AIR.id)
        mc.setBlock(x, y, z, block.AIR.id)
        mc.setBlock(x + 1, y, z, grass_path_id)
        mc.setBlock(x + 1, y, z, grass_path_id)
        z -= 1
        l += 1
    if dir == 0:
        end_points.append([x,y,z, 'posz'])
    else:
        end_points.append([x,y,z, 'negz'])

#function returns coordinates where lammpost will be built
def get_lamppost_coordinates():
    return middle_points

#function takes the coordinates for the door and then joins the door to the path
def join_path(x1, y1, z1, direction, width, depth):
    #checks direction of the door and joins the path accordingly
    if direction == 'posx':
        print(width)
        print(depth)
        # the offset (-4) makes sure the path does not build on the fence surrounding the house
        mc.setBlock(x1, y1 - 2, z1 - 4, block.AIR.id)
        mc.setBlock(x1, y1 - 2, z1 - 4, grass_path_id)
        #function connects the door to the path
        path_negx(x1, y1 - 2, z1 - 4, 5)

    elif direction == 'negx':
        print(width)
        print(depth)
        mc.setBlock(x1, y1 -2, z1 - 4, block.AIR.id)
        mc.setBlock(x1, y1 -2, z1 - 4, grass_path_id)
        #new coordiinate is returned and that point is used to continue the path 
        x,y,z = path_posx(x1, y1 - 2, z1 - 4, width + 2)
        path_posz(x, y, z, depth + 2)

    elif direction == 'posz':
        print(width)
        print(depth)
        # the door is always placed close to the path 
        # these setBlock statements are used to connect the door to the path
        mc.setBlock(x1, y1 - 1, z1 -3, block.AIR.id)
        mc.setBlock(x1, y1 - 1, z1 -3, grass_path_id)
        mc.setBlock(x1 - 1, y1 - 1, z1 -3, grass_path_id)
        mc.setBlock(x1 - 2, y1 - 1, z1 -3, grass_path_id)


    elif direction == 'negz':
        print(width)
        print(depth)
        mc.setBlock(x1, y1 - 1, z1 - 4, block.AIR.id)
        mc.setBlock(x1, y1 - 1, z1 - 4, grass_path_id)
        x,y,z = path_posx(x1, y1, z1 - 4, width + 2)
        x,y,z = path_posz(x,y,z, depth + 7)
        path_negx(x,y,z, 5)

# *********** MAIN *************
def build_path():

    centre = mc.player.getTilePos()

    # check to see if centre in on ground
    ground_x, ground_y, ground_z = getGroundHeight(centre.x, centre.y, centre.z)

    # set player where the path starts to build
    mc.player.setPos(ground_x, ground_y+1, ground_z)


    #storing coordinates of centre ground blocks as lists
    ground_left = [ground_x + 1, ground_y, ground_z]
    ground_right = [ground_x - 1, ground_y, ground_z]
    ground_up = [ground_x, ground_y, ground_z + 1]
    ground_down = [ground_x, ground_y, ground_z - 1]


    #randomly generating the number and length of path
    no_paths = random.randint(3,4)
    print('no of paths:', no_paths)

    center_points = [ground_down, ground_up, ground_left, ground_right]
    # center points with direction for decorations
    center_points_dir = {'negz':ground_down, 'posz':ground_up, 'posx':ground_left, 'negx':ground_right}

    #setting blocks in the centre point of the paths
    mc.setBlock(ground_x, ground_y, ground_z, grass_path_id)
    for i in center_points:
        mc.setBlock(i[0], i[1], i[2], grass_path_id)

    # making path 2 blocks wide
    mc.setBlock(ground_left[0], ground_left[1], ground_left[2] - 1, grass_path_id)
    mc.setBlock(ground_left[0], ground_left[1], ground_left[2] + 1, grass_path_id)
    mc.setBlock(ground_right[0], ground_right[1], ground_right[2] - 1, grass_path_id)
    mc.setBlock(ground_right[0], ground_right[1], ground_right[2] + 1, grass_path_id)    

    # list to store center points that have already been used to create paths
    points_used = []

    for n in range(0,no_paths):
        # Generate a random starting point from center points for the path
        point_picker = random.randint(0,3)

        # Check that the point generated hasn't already been used
        while point_picker in points_used:
            point_picker = random.randint(0,3)

        points_used.append(point_picker)
        # print('points used', points_used)

        # Generate path length
        path_length = random.randint(35, 45)
        print('path length:', path_length)

        # generate paths according to the randomly selected directions
        if point_picker == 0:
            path_negz(center_points[0][0], center_points[0][1], center_points[0][2], path_length)

        elif point_picker == 1:
            path_posz(center_points[1][0], center_points[1][1], center_points[1][2], path_length)

        elif point_picker == 2:
            path_posx(center_points[2][0], center_points[2][1], center_points[2][2], path_length)

        else:
            path_negx(center_points[3][0], center_points[3][1], center_points[3][2], path_length)

    # number of houses to be built
    no_houses = 5

    # number of subpaths to be generated
    no_subpath = no_houses - no_paths
    print('no of subpaths:', no_subpath)

    sub_count = {}

    for i in range(0, len(end_points)):
        sub_count[i] = 0

    for s in range(no_subpath):
        # check if a subpath has already been generated from a main path
        # this helps to make the path more meaningfully connected as it ensures that subpaths are divided eqaullt among main paths
        subpath_start = random.randint(0, no_paths-1)
        sub_count[subpath_start] += 1

        while sub_count[subpath_start] > 1:
            subpath_start = random.randint(0, no_paths-1)
            
        sub_count[subpath_start]+= 1
 
        if end_points[subpath_start][3] == 'posx' or end_points[subpath_start][3] == 'negx':
            subpath_z(ground_x, end_points[subpath_start][0], end_points[subpath_start][1], end_points[subpath_start][2])
        else:
            subpath_x(ground_z, end_points[subpath_start][0], end_points[subpath_start][1], end_points[subpath_start][2])

    return end_points, center_points_dir



    