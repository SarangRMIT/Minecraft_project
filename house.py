from mcpi.minecraft import Minecraft
from mcpi import block
import random

# Connect to Minecraft
mc = Minecraft.create()

storing_list = []
global door_coord_list
door_coord_list = []

def get_door_coord():
    return door_coord_list

#alt_count refers to the alternative split of the rooms ---> odd: acc to depth, even: acc to width
def split_rooms(pos_x, pos_y, pos_z, depth_split, width_split, height_split, alt_count, height, width, depth):
    global storing_list

    #base case 
    if depth == 16 and depth_split == 4:
        return

    #base case
    if width_split < 4 or depth_split < 4:
        #storing_list = [width_split + 1]
        #storing_list.append()
        storing_list.append(width_split + 1)
        if depth % 2 == 0:
            storing_list.append(depth_split * 2)
        else:
            storing_list.append((depth_split * 2) + 1)

        return

    if alt_count % 2 == 0:
        #by width
        mc.setBlocks(pos_x+width_split, pos_y, pos_z, pos_x+width_split, pos_y+height_split, pos_z+depth_split-1, block.BRICK_BLOCK.id)

        #adding a door
        mc.setBlock(pos_x+width_split, pos_y+1, pos_z+depth_split-3, block.DOOR_WOOD.id, 8)
        mc.setBlock(pos_x+width_split, pos_y, pos_z+depth_split-3, block.DOOR_WOOD.id, 0)

        #adding torches on the side of the door
        mc.setBlock(pos_x+width_split-1, pos_y, pos_z+depth_split-2, block.TORCH.id, 5)
        mc.setBlock(pos_x+width_split-1, pos_y, pos_z+depth_split-4, block.TORCH.id, 5)

        #add a second door and more torches if possible
        if depth_split >= 7:
            mc.setBlock(pos_x+width_split, pos_y+1, pos_z+2, block.DOOR_WOOD.id, 8)
            mc.setBlock(pos_x+width_split, pos_y, pos_z+2, block.DOOR_WOOD.id, 0)

            mc.setBlock(pos_x+width_split-1, pos_y, pos_z+1, block.TORCH.id, 5)
            mc.setBlock(pos_x+width_split-1, pos_y, pos_z+3, block.TORCH.id, 5)

        #calling the recursive function
        split_rooms(pos_x, pos_y, pos_z, depth_split//2, width_split-1, height_split, alt_count+1, height, width, depth)

    else:
        #by depth
        mc.setBlocks(pos_x, pos_y, pos_z+depth_split, pos_x+width_split, pos_y+height_split, pos_z+depth_split, block.BRICK_BLOCK.id)
        
        #adding a door 
        mc.setBlock(pos_x+2, pos_y+1, pos_z+depth_split, block.DOOR_WOOD.id, 9)
        mc.setBlock(pos_x+2, pos_y, pos_z+depth_split, block.DOOR_WOOD.id, 1)

        #adding torches on the side of the door
        mc.setBlock(pos_x+1, pos_y, pos_z+depth_split-1, block.TORCH.id, 5)
        mc.setBlock(pos_x+3, pos_y, pos_z+depth_split-1, block.TORCH.id, 5)

        #add a second door and more torches if possible
        if width_split >= 7:
            mc.setBlock(pos_x+width_split-2, pos_y+1, pos_z+depth_split, block.DOOR_WOOD.id, 9)
            mc.setBlock(pos_x+width_split-2, pos_y, pos_z+depth_split, block.DOOR_WOOD.id, 1)

            mc.setBlock(pos_x+width_split-1, pos_y, pos_z+depth_split-1, block.TORCH.id, 5)
            mc.setBlock(pos_x+width_split-3, pos_y, pos_z+depth_split-1, block.TORCH.id, 5)

        #calling the recursive function
        split_rooms(pos_x, pos_y, pos_z+depth_split+1, depth_split, width_split-4, height_split, alt_count+1, height, width, depth)

    #the storing list is used to determine whether after the base case is reached in one half of a room, more rooms can be made to the other half of the space
    list_to_compare = [width_split, depth_split]
    if storing_list == list_to_compare:
        if alt_count % 2 == 1:
            split_rooms(pos_x, pos_y, pos_z, depth_split//2 + 1, width_split-5, height_split, alt_count+1, height, width, depth)
        else:
            split_rooms(pos_x+4, pos_y, pos_z, depth_split//2, width-4, height_split, alt_count+1, height, width, depth)
    

#adding windows along the four walls of the house
def adding_windows(pos_x, pos_y, pos_z, x, z, width, depth):

    while pos_z < z + depth:
        if mc.getBlock(pos_x, pos_y, pos_z+1) == 0 and mc.getBlock(pos_x, pos_y, pos_z+2) == 0 and mc.getBlock(pos_x, pos_y+1, pos_z+1) == 0 and mc.getBlock(pos_x, pos_y+1, pos_z+2) == 0:
            mc.setBlocks(pos_x - 1, pos_y, pos_z + 1, pos_x - 1, pos_y + 1, pos_z + 2, block.GLASS.id)
            pos_z += 4
        else:
            pos_z += 1

    pos_x = x + width - 1
    pos_z = z + 4

    while pos_z < z + depth:
        if mc.getBlock(pos_x, pos_y, pos_z+1) == 0 and mc.getBlock(pos_x, pos_y, pos_z+2) == 0 and mc.getBlock(pos_x, pos_y+1, pos_z+1) == 0 and mc.getBlock(pos_x, pos_y+1, pos_z+2) == 0:
            mc.setBlocks(pos_x + 1, pos_y, pos_z + 1, pos_x + 1, pos_y + 1, pos_z + 2, block.GLASS.id)
            #Adding torches beneath the windows
            mc.setBlocks(pos_x, pos_y - 1, pos_z + 1, pos_x, pos_y - 1, pos_z + 2, block.TORCH.id, 5)
            pos_z += 4
        else:
            pos_z += 1
    
    pos_x = x + 2
    pos_z = z + 4

    while pos_x < x + width:
        if mc.getBlock(pos_x+1, pos_y, pos_z) == 0 and mc.getBlock(pos_x+2, pos_y, pos_z) == 0 and mc.getBlock(pos_x+1, pos_y+1, pos_z) == 0 and mc.getBlock(pos_x+2, pos_y+1, pos_z) == 0:
            mc.setBlocks(pos_x + 1, pos_y, pos_z - 1, pos_x + 2, pos_y + 1, pos_z - 1, block.GLASS.id)
            pos_x += 4
        else:
            pos_x += 1

    pos_x = x + 2
    pos_z = z + 2 + depth

    while pos_x < x + width:
        if mc.getBlock(pos_x+1, pos_y, pos_z) == 0 and mc.getBlock(pos_x+2, pos_y, pos_z) == 0 and mc.getBlock(pos_x+1, pos_y+1, pos_z) == 0 and mc.getBlock(pos_x+2, pos_y+1, pos_z) == 0:
            mc.setBlocks(pos_x + 1, pos_y, pos_z + 1, pos_x + 2, pos_y + 1, pos_z + 1, block.GLASS.id)
            pos_x += 4
        else:
            pos_x += 1


#adding furniture inside the rooms 
def adding_furniture(x, y, z, width, depth):
    #Setting the carpet block - 171 is the block id for carpet
    #Randomising the color of the carpet used
    mc.setBlocks(x + 6, y, z + 3 + depth//2 - 2, x + 10, y, z + 3 + depth//2 - 3, 171, random.randint(0, 15))

    #Adding a bed in one of the rooms
    mc.setBlock(x + 7, y, z + 4 + depth//2, block.BED.id, 9)
    mc.setBlock(x + 8, y, z + 4 + depth//2, block.BED.id, 1)

    #Adding furniture in the rest of the rooms
    pos_z = z + 2 + depth
    pos_x = x + 2

    while pos_x + 2 < x + width:
        #Randomising what furniture item is used
        furniture_item = random.randint(1, 3)

        if mc.getBlock(pos_x, y, pos_z) == 0 and mc.getBlock(pos_x + 1, y, pos_z) == 0:
            if furniture_item == 1:
                mc.setBlocks(pos_x, y, pos_z, pos_x + 1, y, pos_z, block.CHEST.id)
            if furniture_item == 2:
                mc.setBlocks(pos_x, y, pos_z, pos_x + 1, y, pos_z, block.BOOKSHELF.id)
            if furniture_item == 3:
                mc.setBlocks(pos_x, y, pos_z, pos_x + 1, y, pos_z, block.CRAFTING_TABLE.id)
            pos_x += 4
    
        else:
            pos_x += 1

    #Adding extra torches
    if mc.getBlock(x + width - 9, y, z + 4) == 0 and mc.getBlock(x + width - 8, y, z + 4) == 0:
        mc.setBlocks(x + width - 9, y, z + 4, x + width - 8, y, z + 4, block.TORCH.id, 5)


## MAIN FUNCTION ##
def build_house(pos_x, pos_y, pos_z, width, depth):
    x = pos_x
    y = pos_y
    z = pos_z

    #Determining the height of the house to determine the number of stories in the house
    height_determiner = random.randint(1, 2)
    if height_determiner == 1:
        height = 4                                  #one story house
    else:
        height = 9                                  #two story house

    ### HOUSE - EXTERIOR ###
    #Laying the foundation for the house
    mc.setBlocks(x-2, y-1, z+1, x+2+width, y-1, z+5+depth, block.COBBLESTONE.id)

    #Adding a fence around the house
    mc.setBlocks(x-2, y, z+1, x+2+width, y, z+1, block.FENCE.id)
    mc.setBlocks(x-2, y, z+1, x-2, y, z+5+depth, block.FENCE.id)
    mc.setBlocks(x+2+width, y, z+5+depth, x+2+width, y, z+1, block.FENCE.id)
    mc.setBlocks(x-2, y, z+5+depth, x+2+width, y, z+5+depth, block.FENCE.id)

    #Adding a fence gate in front of the front door
    mc.setBlock(x+1, y, z+1, block.FENCE_GATE.id)

    #Adding the house block and then hollowing it out
    mc.setBlocks(x, y, z+3, x+width, y+height, z+3+depth, block.BRICK_BLOCK.id)
    mc.setBlocks(x+1, y, z+4, x+width-1, y+height-1, z+2+depth, block.AIR.id)

    #Adding the front door of the house
    mc.setBlock(x+1, y+1, z+3, block.DOOR_WOOD.id, 9)
    mc.setBlock(x+1, y, z+3, block.DOOR_WOOD.id, 1)

    door_coord = [x+1, y+1, z+3]
    door_coord_list.append(door_coord)
    

    ### ROOF ###
    #Generating a random number to determine which type of roof the house will have
    roof_type = random.randint(1,2)

    if roof_type == 1:
        #Roof type 1 : slanting roof
        mc.setBlocks(x-1, y+height-1, z+3, x-1, y+height-1, z+3+depth, block.WOOD_PLANKS.id)
        mc.setBlocks(x+width+1, y+height-1, z+3, x+width+1, y+height-1, z+3+depth, block.WOOD_PLANKS.id)

        for i in range(int(width/2) + 1):
            mc.setBlocks(x+i, y+height+i, z+3, x+i, y+height+i, z+3+depth, block.WOOD_PLANKS.id)
            mc.setBlocks(x+width-i, y+height+i, z+3, x+width-i, y+height+i, z+3+depth, block.WOOD_PLANKS.id)
            if (int(width/2) - i > 0):
                mc.setBlocks(x+1+i, y+height+i, z+3, x+width-i-1, y+height+i, z+3, block.BRICK_BLOCK.id, 0)
                mc.setBlocks(x+1+i, y+height+i, z+3+depth, x+width-i-1, y+height+i, z+3+depth, block.BRICK_BLOCK.id, 1)

    else:
        #Roof type 2 : flat roof with levels
        mc.setBlocks(x-1, y+height+1, z+2, x+width+1, y+height+1, z+4+depth, block.WOOD_PLANKS.id)
        mc.setBlocks(x, y+height+2, z+3, x+width, y+height+2, z+3+depth, block.WOOD_PLANKS.id)

        for i in range(1, width//2 + 1):
            if 3+i < 3+depth-i:
                mc.setBlocks(x+i, y+height+2+i, z+3+i, x+width-i, y+height+2+i, z+3+depth-i, block.WOOD_PLANKS.id)
            else:
                break


    ### HOUSE - INTERIOR ###
    if height == 4:
        #add a ground block
        mc.setBlocks(x+1, y-1, z+4, x+width-1, y-1, z+2+depth, block.WOOD_PLANKS.id)
        #add a ceiling block
        mc.setBlocks(x+1, y+4, z+4, x+width-1, y+4, z+2+depth, block.WOOD_PLANKS.id)

        #splitting of the rooms
        split_rooms(x, y, z+3, depth//2, width, 3, 1, height, width, depth)

        #adding windows
        adding_windows(x+1, y+1, z+4, x, z, width, depth)

        #adding furniture
        adding_furniture(x, y, z, width, depth)

    else:
        #add a ground block
        mc.setBlocks(x+1, y-1, z+4, x+width-1, y-1, z+2+depth, block.WOOD_PLANKS.id)
        # add a first floor block
        mc.setBlocks(x+1, y+4, z+4, x+width-1, y+4, z+2+depth, block.WOOD_PLANKS.id)
        #add a ceiling block
        mc.setBlocks(x+1, y+9, z+4, x+width-1, y+9, z+2+depth, block.WOOD_PLANKS.id)
        
        #making hole in the wall of the first floor for the stairs
        mc.setBlocks(x+width-3, y+4, z+4, x+width-6, y+4, z+5, block.AIR.id)

        #adding the stairs
        for i in range(0, 4):
            mc.setBlock(x+width-6+i, y+i, z+4, block.STAIRS_WOOD.id)
            mc.setBlock(x+width-6+i, y+i, z+5, block.STAIRS_WOOD.id)

        #splitting the rooms for the ground floor
        split_rooms(x, y, z+3, depth//2, width, 3, 1, height, width, depth)

        #clearing the list to split the rooms for the first floor
        storing_list.clear()

        #splitting the rooms for the first floor
        split_rooms(x, y+5, z+3, depth, 4, 3, 2, height, width, depth)

        #adding windows
        adding_windows(x+1, y+1, z+4, x, z, width, depth)             #ground floor
        adding_windows(x+1, y+6, z+4, x, z, width, depth)             #first floor

        #adding furniture
        adding_furniture(x, y, z, width, depth)                       #ground floor
        adding_furniture(x, y+5, z, width, depth)                     #first floor