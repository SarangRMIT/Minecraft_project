from operator import truediv
from mcpi import minecraft
from mcpi import block
import random

end_points = []

mc = minecraft.Minecraft.create()

# Find actual ground level (not on top of trees, etc.)
def getGroundHeight(x,z):
    # types of blocks that the road shouldn't be built on
    nonGroundBlocks = [block.WOOD_PLANKS.id, block.STONE.id, block.WATER.id, block.AIR.id, block.SAPLING.id, block.ICE.id, 
        block.CACTUS.id, block.LEAVES.id, block.WOOD.id,
        block.FLOWER_CYAN.id, block.FLOWER_YELLOW.id]

    # current block type
    height = mc.getHeight(x,z)
    blocktype = mc.getBlockWithData(x,height,z)
    # print(blocktype)
    while blocktype.id in nonGroundBlocks:
            x += 1
            height = mc.getHeight(x,z)
            blocktype = mc.getBlockWithData(x,height,z)
    mc.player.setPos(x, height+1, z)
    
    return x,height,z


#checks if the block is grass, sand, dirt etc so path can be built on it
#returns false if block is part of not valid list
def validBlock(check_block):
    not_valid = [block.WATER.id, block.AIR.id, block.SAPLING.id, block.ICE.id, 
        block.CACTUS.id, block.LEAVES.id, block.LAVA.id, block.LAVA_FLOWING.id, block.LAVA_STATIONARY.id, 
        block.WOOD.id, block.WOOD_PLANKS.id]
    if check_block in not_valid:
        return False
    else:
        return True
def non_valid_object(object):
    not_valid_objects=[block.SAPLING.id,block.CACTUS.id,block.LEAVES.id,block.WOOD.id]
    if object in not_valid_objects:
        return True
    else:
        return False

def pickBlock():
    #randomly generates direction of path
    # left = 0, right = 1, up = 2, down = 3
    direction = random.randint(0,3)
    return direction

def direction(c):
    #randomly moves along x/z axis
    direction = random.randint(0,1)
    if direction == 0:
        #north or east
        c -= 1
    else:
        #south or west
        c += 1 
    return c

def buildPath(x,y,z):
    blocktype = mc.getBlock(x,y,z)
    if mc.getBlock(x,y,z) == blocktype:
        if (mc.getBlock(x, y + 1, z) == block.AIR.id):
            mc.setBlock(x, y, z, block.IRON_BLOCK.id)
        else:
            if validBlock(mc.getBlock(x,y,z)):
                mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
    else:
        if validBlock(mc.getBlock(x,y,z + 1)) == True:
            mc.setBlock(x, y, z+1, block.IRON_BLOCK.id)
        elif validBlock(mc.getBlock(x,y,z-1)) == True:
            mc.setBlock(x, y, z-1, block.IRON_BLOCK.id)


#function receives path lenght and coordinates of the starting block
def setPathRight(path_length, x, y, z):
    global end_points
    #randomly generating the length of the path
    for i in range(path_length): 
        #checking for obstacles trees, flowers, water etc
        buildPath(x,y,z)
        if validBlock(mc.getBlock(x,y,z)) == True:
            if (mc.getBlock(x, y + 1, z) == block.AIR.id):
                mc.setBlock(x, y, z, block.IRON_BLOCK.id)
            else:
                #meets an obstacle
                print('in right else')
                if non_valid_object(mc.getBlock(x,y+1,z)==True):
                    height=mc.getHeight(x,z)
                    mc.setBlocks(x,y,z,x,y+10 ,z,block.AIR)
                if validBlock(mc.getBlock(x,y + 1,z)) == True:
                    mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y,z-1)) == True:
                    mc.setBlock(x, y, z-1, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y, z + 1)) == True:
                    mc.setBlock(x, y, z + 1, block.IRON_BLOCK.id)
        #increasing the x value to create the path
        x += 1
    #stores list of end points of the path, used to build houses 
    end_points.append([x,y,z])

def setPathLeft(path_length, x, y, z):
    global end_points
    #randomly generating the length of the path
    for i in range(path_length): 
        #checking for obstacles trees, flowers, water etc
        buildPath(x,y,z)
        if validBlock(mc.getBlock(x,y,z)) == True:
            if (mc.getBlock(x, y + 1, z) == block.AIR.id):
                mc.setBlock(x, y, z, block.IRON_BLOCK.id)
            else:
                #meets an obstacle
                print('in left else')
                if non_valid_object(mc.getBlock(x,y+1,z)==True):
                    height=mc.getHeight(x,z)
                    mc.setBlocks(x,y,z,x,y+10 ,z,block.AIR)
                if validBlock(mc.getBlock(x,y + 1,z)) == True:
                    mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y,z-1)) == True:
                    mc.setBlock(x, y, z-1, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y, z + 1)) == True:
                    mc.setBlock(x, y, z + 1, block.IRON_BLOCK.id)
        #increasing the x value to create the path
        x -= 1
    #stores list of end points of the path, used to build houses 
    end_points.append([x,y,z])

def setPathNorth(path_length, x, y, z):
    global end_points
    #randomly generating the length of the path
    for i in range(path_length): 
        buildPath(x,y,z)
        #checking for obstacles trees, flowers, water etc
        if validBlock(mc.getBlock(x,y,z)) == True:
            if (mc.getBlock(x, y + 1, z) == block.AIR.id):
                mc.setBlock(x, y, z, block.IRON_BLOCK.id)
            else:
                #meets an obstacle
                print('in north else')
                if non_valid_object(mc.getBlock(x,y+1,z)==True):
                    height=mc.getHeight(x,z)
                    mc.setBlocks(x,y,z,x,y+10 ,z,block.AIR)
                if validBlock(mc.getBlock(x,y + 1,z)) == True:
                    mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y,z-1)) == True:
                    mc.setBlock(x, y, z-1, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y, z + 1)) == True:
                    mc.setBlock(x, y, z + 1, block.IRON_BLOCK.id)
        #increasing the x value to create the path
        z += 1
    #stores list of end points of the path, used to build houses 
    end_points.append([x,y,z])

def setPathSouth(path_length, x, y, z):
    global end_points
    #randomly generating the length of the path
    for i in range(path_length): 
        buildPath(x,y,z)
        #checking for obstacles trees, flowers, water etc
        if validBlock(mc.getBlock(x,y,z)) == True:
            if (mc.getBlock(x, y + 1, z) == block.AIR.id):
                mc.setBlock(x, y, z, block.IRON_BLOCK.id)
            else:
                #meets an obstacle
                print('in south else')
                if non_valid_object(mc.getBlock(x,y+1,z)==True):
                    height=mc.getHeight(x,z)
                    mc.setBlocks(x,y,z,x,y+10 ,z,block.AIR)
                if validBlock(mc.getBlock(x,y + 1,z)) == True:
                    mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y,z-1)) == True:
                    mc.setBlock(x, y, z-1, block.IRON_BLOCK.id)
                elif validBlock(mc.getBlock(x,y, z + 1)) == True:
                    mc.setBlock(x, y, z + 1, block.IRON_BLOCK.id)
        #increasing the x value to create the path
        z -= 1
    #stores list of end points of the path, used to build houses 
    end_points.append([x,y,z])

#bulids path from the middle of another path
def subPath(offset, x,y,z):
    # left = 0, right = 1, up = 2, down = 3
    path_length = random.randint(10,20)
    direction = pickBlock()
    if direction == 0:
        #left
        x -= offset
        setPathRight(path_length, x, y, z)
    elif direction == 1:
        #right
        x += offset
        setPathRight(path_length, x, y, z)
    elif direction == 2:
        #up
        z -= offset
        setPathSouth(path_length, x, y, z)
    elif direction == 3:
        #down
        z += offset
        setPathNorth(path_length, x, y, z)

centre = mc.player.getTilePos()
# check to see if centre in on ground
ground_x, ground_y, ground_z = getGroundHeight(centre.x, centre.z)

#storing coordinates of centre ground blocks as lists 
ground_left = [ground_x + 1, ground_y, ground_z]
ground_right = [ground_x - 1, ground_y, ground_z]
ground_up = [ground_x, ground_y, ground_z + 1]
ground_down = [ground_x, ground_y, ground_z - 1]

#list of four centre coordinates
coordinates = [ground_left, ground_right, ground_up, ground_down]

#setting blocks in the centre point of the paths 
mc.setBlock(ground_x, ground_y, ground_z, block.DIAMOND_BLOCK.id)
for i in range(len(coordinates)):
    mc.setBlock(coordinates[i][0], coordinates[i][1], coordinates[i][2], block.DIAMOND_BLOCK.id)

#randomly generating the number and length of path
no_paths = random.randint(2,4)

points_used = []
#calling function to set paths
print('number of paths', no_paths)
for i in range(no_paths):
    path_length = random.randint(10,20)
    print('path length', path_length)
    
    # b is the block the path will be built on
    b = pickBlock()
    while b in points_used:
        b = pickBlock()
    points_used.append(b)
    print('direction', b)

    if b == 0:
        #left
        setPathLeft(path_length, coordinates[b][0], coordinates[b][1], coordinates[b][2])
    elif b == 1:
        #right
        setPathRight(path_length, coordinates[b][0], coordinates[b][1], coordinates[b][2])
    elif b == 2:
        #up
        setPathNorth(path_length, coordinates[b][0], coordinates[b][1], coordinates[b][2])
    elif b == 3:
        #down
        setPathSouth(path_length, coordinates[b][0], coordinates[b][1], coordinates[b][2])

print(end_points)

# #randomly generating the number and length of sub paths
# no_subpaths = random.randint(1,3)
# print('number of subpaths', no_subpaths)
# for i in range(no_subpaths):
#     offset = random.randint(2,4)
#     print('offset', offset)
#     #calling function to set sub paths
#     subPath(offset, end_points[i][0], end_points[i][1], end_points[i][2])
# print(end_points)