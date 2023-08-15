from mcpi.minecraft import Minecraft
import random
import path
import teraforming
import house
import decorations

mc = Minecraft.create()

#stores dimensions of the house to send to the join path function
global dim
dim = []

#stores coordinates of the end point of the path to build houses
#centre points are stored to build fountain near it
house_coordinates, center_points = path.build_path()
print(house_coordinates)

for i in house_coordinates:
    #width and depth of the house is randomised and sent to house building function
    width = random.randint(13, 20)
    depth = random.randint(12, 19)
    dim.append([width, depth])
    print(f'width: {width}, depth: {depth}')

    #area which house will be built on is terraformed according to the direction of the path
    if i[3] == 'posx' or i[3] == 'posz':
        print("teraforming starting")
        teraforming.teraform_land(i[3],i[0]+2,i[1]+1,i[2]-2, width, depth)
        print("teraforming ending")

        print("building house")
        house.build_house(i[0]+2,i[1]+1,i[2]-1, width, depth)
        print("finished house")

    elif i[3] == 'negx' or i[3] == 'negz':
        print("teraforming starting")
        teraforming.teraform_land(i[3],i[0]-width+1,i[1]+1,i[2]-depth-1, width, depth)
        print("teraforming ending")

        print("building house")
        house.build_house(i[0]-width+1,i[1] + 1,i[2]-depth-1, width, depth)
        print("finished house")

    elif i[3] == 'negz':
        print("teraforming starting")
        teraforming.teraform_land(i[3],i[0]-width+1,i[1]+1,i[2]-depth-1, width, depth)
        print("teraforming ending")

    print('dir:',i[3])

#door coordinates are stored to send to join path function
door_points = house.get_door_coord()
print(door_points)

#door is connected to the path
for i in range(0,5):
    print('joining path in direction:', house_coordinates[i][3])
    path.join_path( door_points[i][0], door_points[i][1]-1, door_points[i][2], house_coordinates[i][3], dim[i][0], dim[i][1])


print('adding decorations')
#adding lamposts
lamppost_coordinates = path.get_lamppost_coordinates()
for j in range(0,3):
    decorations.addLampPost(lamppost_coordinates[j][0],lamppost_coordinates[j][1],lamppost_coordinates[j][2])

# adding pool, garden, animal pen for a random number of houses
no_houses = random.randint(3,5)
print('no house decos:', no_houses)

for n in range(0,no_houses):
    deco_type = random.randint(1,3)
    print('deco type:', deco_type)
    

    if house_coordinates[n][3] == 'posx' or house_coordinates[n][3] == 'posz':
        # generate a random number to pick a decoration
        deco_type = random.randint(1,3)
        if deco_type == 1:
            decorations.pool(house_coordinates[n][0]+width+10, house_coordinates[n][1], house_coordinates[n][2], house_coordinates[n][3])
        elif deco_type == 2:
            decorations.flowerGarden(house_coordinates[n][0]+width+10, house_coordinates[n][1], house_coordinates[n][2], house_coordinates[n][3])
        else:
            decorations.animalPen(house_coordinates[n][0]+width+10, house_coordinates[n][1], house_coordinates[n][2], house_coordinates[n][3])

    elif house_coordinates[n][3] == 'negx' or house_coordinates[n][3] == 'negz':
        # generate a random number to pick a decoration
        deco_type = random.randint(1,3)
        if deco_type == 1:
            decorations.pool(house_coordinates[n][0]-2, house_coordinates[n][1], house_coordinates[n][2]-depth-10, house_coordinates[n][3])
        elif deco_type == 2:
            decorations.flowerGarden(house_coordinates[n][0]-2, house_coordinates[n][1], house_coordinates[n][2]-depth-10, house_coordinates[n][3])
        else:
            decorations.animalPen(house_coordinates[n][0]-2, house_coordinates[n][1], house_coordinates[n][2]-depth-10, house_coordinates[n][3])


# adding fountain near the village centre
point_picker = random.randint(0,3)
center_points_keys = list(center_points.keys())

if center_points_keys[point_picker] == 'posx':
    decorations.fountain(center_points['posx'][0]+6,center_points['posx'][1],center_points['posx'][2]+6)

elif center_points_keys[point_picker] == 'negx':
    decorations.fountain(center_points['negx'][0]-6,center_points['negz'][1],center_points['negz'][2]+6)

elif center_points_keys[point_picker] == 'posz':
    decorations.fountain(center_points['posz'][0]+6,center_points['posz'][1],center_points['posz'][2]+6)

elif center_points_keys[point_picker] == 'negz':
    decorations.fountain(center_points['negz'][0]-6,center_points['negz'][1],center_points['negz'][2]-6)

print('made fountain', center_points_keys[point_picker])