from audioop import avg
from mcpi import minecraft
from mcpi import block
#from path_Aayushi import getGroundHeight
mc = minecraft.Minecraft.create()
# x, y, z = mc.player.getPos()
global x, y, z
# h=mc.getHeight(x,z)
# print(h)

def basic_teraforming():
    mc.setBlocks(x-15,y,z-15,x+15,y+100 ,z+15,block.AIR) 

def check_location(length, x,y,z):
    x_axis_heights = []
    y_axis_heights = []

    # global x,y,z
    temp_x,temp_y,temp_z=x,y,z
    # x-axis
    for i in range(0,length):
        h_x=mc.getHeight(temp_x,z)
        x_axis_heights.append(h_x)
        temp_x+=1
    # negative x-axis
    temp_x=x #reseting x coordinate to initial position
    for i in range(0,length):
        h_x=mc.getHeight(temp_x,z)
        x_axis_heights.append(h_x)
        temp_x-=1
    # y-axis
    for i in range(0,length):
        h_y=mc.getHeight(x,temp_z)
        y_axis_heights.append(h_y)
        temp_z+=1
    # negative y-axis
    temp_z=z #reseting y coordinate to initial position
    for i in range(0,length):
        h_y=mc.getHeight(x,temp_z)
        y_axis_heights.append(h_y)
        temp_z-=1
    combined_height= y_axis_heights+x_axis_heights
    location={}
    avg=sum(combined_height)/len(combined_height)
    location["max_height"]=max(combined_height)
    location["avg_height"]=avg
    return location

# teraforming for decorations
def decorations_teraforming(x,y,z,x2,z2):
    mc.setBlock(x,y,z,x2,y+70,z2, block.AIR)

def teraform_land(dir,x_,y_,z_, width, depth):
    # width=15
    # length=15
    
    x,y,z = x_,y_,z_
    blockid=mc.getBlock(x,y-1,z)
    # h=mc.getHeight(x,z)
    # mc.getHeight(x+(depth//2),z+width//2)
    # dictionary=check_location(20, x,y,z)
    # if (dictionary["max_height"]-dictionary["avg_height"])<5:
    # mc.setBlocks(x-2, y-1, z+1, x+2+width, y+70, z+5+depth,block.AIR)
    
    
    # teraforming land for the houses according to the direction the respective path was built in
    if dir == 'posx':
        mc.setBlocks(x-2, y-1, z-3, x+2+width, y+70, z+10+depth,block.AIR)
        mc.setBlocks(x-2, y-2, z-3, x+2+width, y-1, z+10+depth,block.GRASS)
    #     # dictionary=check_location(20, x,y,z)
    #     # if (dictionary["max_height"]-dictionary["avg_height"])<5:
    #     #     mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)
    #     # else:
    #     #     mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)

    elif dir == 'negx':
        mc.setBlocks(x-2, y-1, z-3, x+2+width, y+70, z+5+depth,block.AIR)
        mc.setBlocks(x-2, y-2, z-3, x+2+width, y-1, z+5+depth,block.GRASS)
    #     dictionary=check_location(20, x,y,z)
    #     if (dictionary["max_height"]-dictionary["avg_height"])<5:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)
    #     else:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)

    elif dir == 'posz':
        mc.setBlocks(x-5, y-1, z+1, x+5+width, y+70, z+5+depth,block.AIR)
        mc.setBlocks(x-5, y-2, z+1, x+5+width, y-1, z+5+depth,block.GRASS)

    #     dictionary=check_location(20,  x,y,z)
    #     if (dictionary["max_height"]-dictionary["avg_height"])<5:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)
    #     else:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["avg_height"]+25,z+30,block.AIR)

    elif dir == 'negz':
        mc.setBlocks(x-5, y-1, z+1, x+5+width, y+70, z+5+depth,block.AIR)
        mc.setBlocks(x-5, y-2, z+1, x+5+width, y-1, z+5+depth,block.GRASS)

    #     dictionary=check_location(20,  x,y,z)
    #     if (dictionary["max_height"]-dictionary["avg_height"])<5:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)
    #     else:
    #         mc.setBlocks(x-5,y-1,z,x+25,y+dictionary["max_height"]+25,z+30,block.AIR)

    
    
