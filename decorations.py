from mcpi import minecraft
from mcpi import block
import random
from mcpi import entity
import teraforming


'''
---- Decorations that can be made --- 
Pool
Flower garden
Animal pen
Trees
Lampost
Fountain
'''
sea_lantern_id = 169
mc = minecraft.Minecraft.create()

def pool(x, y, z, dir):
    length = random.randint(10,15)
    width = random.randint(8,10)
    depth = random.randint(3,7)

    if dir == 'posx' or dir == 'posz':
        teraforming.decorations_teraforming(x,y,z,x+length,z+width)
        mc.setBlocks(x, y, z, x+length, y-depth, z+width, block.AIR.id)
        mc.setBlocks(x, y-depth, z, x+length, y-depth, z+width, block.STONE)
        mc.setBlocks(x, y-1, z, x+length, y-depth, z, block.STONE)
        mc.setBlocks(x, y-1, z, x, y-depth, z+width, block.STONE)
        mc.setBlocks(x+length, y-1, z, x+length, y-depth, z+width, block.STONE)
        mc.setBlocks(x, y-1, z+width, x+length, y-depth, z+width, block.STONE)
        mc.setBlocks(x+1,y-2,z+1, x+length-1, y-depth+1, z+width-1, block.WATER_FLOWING)

    else:
        teraforming.decorations_teraforming(x,y,z,x-length,z-width)
        mc.setBlocks(x, y, z, x-length, y-depth, z-width, block.AIR.id)
        mc.setBlocks(x, y-depth, z, x-length, y-depth, z-width, block.STONE)
        mc.setBlocks(x, y-1, z, x-length, y-depth, z, block.STONE)
        mc.setBlocks(x, y-1, z, x, y-depth, z-width, block.STONE)
        mc.setBlocks(x-length, y-1, z, x-length, y-depth, z-width, block.STONE)
        mc.setBlocks(x, y-1, z-width, x-length, y-depth, z-width, block.STONE)
        mc.setBlocks(x-1,y-2,z-1, x-length+1, y-depth+1, z-width+1, block.WATER_FLOWING)

def flowerGarden(x, y, z, dir):
    length = random.randint(5,10)
    width = random.randint(5,10)

    flowers = [block.FLOWER_CYAN.id, block.FLOWER_YELLOW.id, 37, 38, 175, (38,1),(38,2),(38,3),(38,4),(38,5), (175,1),(175,2),(175,3),(175,4),(175,5)]

    pick_flower = random.randint(0, len(flowers)-1)

    if dir == 'posx' or dir == 'posz':
        teraforming.decorations_teraforming(x, y, z, x+length, z+width)
        mc.setBlocks(x, y-1, z, x+length, y-1, z+width, block.DIRT)
        mc.setBlocks(x, y, z, x+length, y, z+width, flowers[pick_flower])

        # fence around garden
        mc.setBlocks(x, y, z, x+length, y, z, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z, x, y, z+width, block.FENCE_DARK_OAK)
        mc.setBlocks(x+length, y, z, x+length, y, z+width, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z+width, x+length, y, z+width, block.FENCE_DARK_OAK)

    else:
        teraforming.decorations_teraforming(x, y, z, x-length, z-width)
        mc.setBlocks(x, y-1, z, x-length, y-1, z-width, block.DIRT)
        mc.setBlocks(x, y, z, x-length, y, z-width, flowers[pick_flower])

        # fence around garden
        mc.setBlocks(x, y, z, x-length, y, z, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z, x, y, z-width, block.FENCE_DARK_OAK)
        mc.setBlocks(x-length, y, z, x-length, y, z-width, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z-width, x-length, y, z-width, block.FENCE_DARK_OAK)


def animalPen(x,y,z, dir):
    length = random.randint(5,10)
    width = random.randint(5,10)
    no_animals = random.randint(3, 5)

    animals = [entity.CHICKEN, entity.COW, entity.HORSE, entity.PIG, entity.RABBIT]

    animal_picker = random.randint(0, len(animals)-1)

    if dir == 'negx' or dir == 'negz':
        teraforming.decorations_teraforming(x, y, z, x-length, z-width)
        mc.setBlocks(x, y-1, z, x-length, y-1, z-width, block.DIRT)

        # fence around pen
        mc.setBlocks(x, y, z, x-length, y, z, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z, x, y, z-width, block.FENCE_DARK_OAK)
        mc.setBlocks(x-length, y, z, x-length, y, z-width, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z-width, x-length, y, z-width, block.FENCE_DARK_OAK)

        # spawn animals
        for a in range(no_animals):
            mc.spawnEntity(x-3,y,z-3, animals[animal_picker])
            if x > x-length:
                x -=1
            else: z-=1

    else:
        teraforming.decorations_teraforming(x, y, z, x+length, z+width)
        mc.setBlocks(x, y-1, z, x+length, y-1, z+width, block.DIRT)

        # fence around pen
        mc.setBlocks(x, y, z, x+length, y, z, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z, x, y, z+width, block.FENCE_DARK_OAK)
        mc.setBlocks(x+length, y, z, x+length, y, z+width, block.FENCE_DARK_OAK)
        mc.setBlocks(x, y, z+width, x+length, y, z+width, block.FENCE_DARK_OAK)

        # spawn animals
        for a in range(no_animals):
            mc.spawnEntity(x+3,y,z+3, animals[animal_picker])
            if x < x+length:
                x +=1
            else: z+=1


def addLampPost(x,y,z):
    z += 2
    #setting post
    mc.setBlock(x,y,z,block.STONE)
    mc.setBlocks(x, y + 1, z, x, y + 5, z, block.FENCE_DARK_OAK)
    #adding light
    mc.setBlock(x - 1, y + 5, z, sea_lantern_id)
    mc.setBlock(x + 1, y + 5, z, sea_lantern_id)
    mc.setBlock(x, y + 5, z + 1, sea_lantern_id)
    mc.setBlock(x, y + 5, z - 1, sea_lantern_id)
    

# x,y,z = mc.player.getTilePos()
# # addLampPost(x,y,z)
# pool(x,y,z, 'negz')
# flowerGarden(x,y,z)
#AnimalPen(x,y,z)

def fountain(x,y,z):
    base=5
    width=3
    mc.setBlocks(x-3,y,z-3,x+3,y,z+3,block.STONE)
    mc.setBlocks(x-2,y,z-2,x+2,y,z+2,block.AIR)
    mc.setBlocks(x-2,y-1,z-2,x+2,y-1,z+2,block.STONE)
    mc.setBlocks(x,y,z,x,y+2,z,block.BEDROCK)
    mc.setBlock(x,y+3,z,block.WATER_FLOWING)
    #mc.setBlock(x,y+2,z,block.WATER_FLOWING)
# fountain(x,y,z)
