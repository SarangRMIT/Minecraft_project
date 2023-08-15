from mcpi import minecraft
from mcpi import block
import random

end_points = []

mc = minecraft.Minecraft.create()

# Find actual ground level (not on top of trees, etc.)
def getGroundHeight(x,z):
    # types of blocks that the road shouldn't be built on
    nonGroundBlocks = [block.WATER.id, block.AIR.id, block.SAPLING.id, block.ICE.id, 
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
        block.CACTUS.id, block.LEAVES.id, block.WOOD.id]
    if check_block in not_valid:
        return False
    else:
        return True

 #function receives path length and coordinates of the starting block

def setPath(path_length, x, y, z):
    #randomly generating the length of the path
    for i in range(path_length):
        #checking for obstacles trees, flowers, water etc
        if validBlock(mc.getBlockWithData(x,y,z)) == True:
                mc.setBlock(x, y + 1, z, block.IRON_BLOCK.id)
        else:
            #meets an obstacle
            z = direction(z)
            validBlock(mc.getBlock(x,y,z))
        #increasing the x value to create the path
        x += 1

def direction(z):
    #randomly generates direction
    direction = random.randint(0,1)
    if direction == 0:
        #north
        z += 1
    else:
        #east
        z -= 1
    return z

centre = mc.player.getTilePos()

# check to see if centre in on ground
ground_x, ground_y, ground_z = getGroundHeight(centre.x, centre.y, centre.z)
#storing coordinates of centre ground blocks as lists
ground_left = [ground_x + 1, ground_y, ground_z]
ground_right = [ground_x - 1, ground_y, ground_z]
ground_up = [ground_x, ground_y, ground_z + 1]
ground_down = [ground_x, ground_y, ground_z - 1]

#randomly generating the number and length of path
no_paths = random.randint(2,4)
path_length = random.randint(10,20)
#setting blocks in the centre point of the paths
mc.setBlock(ground_x, ground_y, ground_z, block.DIAMOND_BLOCK.id)
mc.setBlock(ground_left[0], ground_left[1], ground_left[2], block.DIAMOND_BLOCK.id)
mc.setBlock(ground_right[0], ground_right[1], ground_right[2], block.DIAMOND_BLOCK.id)
mc.setBlock(ground_up[0], ground_up[1], ground_up[2], block.DIAMOND_BLOCK.id)
mc.setBlock(ground_down[0], ground_down[1], ground_down[2], block.DIAMOND_BLOCK.id)