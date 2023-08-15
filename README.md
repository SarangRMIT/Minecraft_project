[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8376003&assignment_repo_type=AssignmentRepo)
# Minecraft Village
This is the README file for Assignment 1 in Programming Studio 2 (COSC2804).

Please indicate where to find your video presentation. You can include it in this repo if it's small enough, or alternatively use a video sharing platform, such as YouTube. Any widely supported video format is fine (.mp4, .avi, .mkv, etc.)

Ignore and do not modify the contents of the .devcontainer folder. (In case it is not possible to run a Minecraft server locally, the repo is setup to work with GitHub Codespaces as a backup.)


# Seeds 
- Seeds in which our village works well (if you spawn in water, please find the nearest ground block to run the code. Does not have to be a massive piece of land, even a small island works):
    - 8614262653530851772
    - 7024803338332632605
    - 4504535438041489910
    - 3257840388504953787

# Mandatory: Student contributions
Please summarise each team member's contributions here. Include both an approximate, percentage-based breakdown (e.g., "Anna: 25%, Tom: 25%, Claire: 25%, Halil: 25%") **and a high-level summary of what each member worked on, in dot-point form**.

Ideally, any disputes reagarding the contributions should be resolved prior to submission, but if there is an unresolved dispute then please indicate that this is the case. Do not override each other's contribution statements immediately prior to the deadline -- this will be viewed dimly by the markers!

# Individual Contributions

Akshita Agrawal: 25%
- Responsible for building the houses   
- Made the basic structure of the house : walls, doors, windows, roofs  
- Made a working recursive function for splitting the rooms inside the houses  
- Made multiple stories for the houses and connecting the stories with stairs   
- Decorated the houses by adding furniture in them, and adding a fence with a fence gate around them  
- Randomised various aspects of the house:  
    - The lengths and widths of the house  
    - The height of the houses to determine how many stories it will contain  
    - What type of roof should the house contain  
    - The color of some types of furniture, or what type of furniture should be places  

Penusha Udapamunuwa: 25%
- Created paths according to Aayushi's center point method
- Wrote the code so that it randomly generates a number for main paths based on the number of houses
- Then it randomly picks a direction along the x axis or z axis and builds the path accordingly
- After that, for the remaining houses, it picks a direction once more and generates subpaths 
- It also checks the blocks above and below and forms steps going up or down if it reaches a hilly area
- For the decorations file, created code for pool, animal pen and flower garden
- Implemented pool, animal pen, flower garden and fountain so that they are randomly and sensibly placed within the village layout
- Wrote part of the code to make the houses fit in with the teraforming when combined

Aayushi Khatri: 25%
- Worked alongside Penusha to implement the paths and village road network.
- We iterated through a few approaches but settled on spawning the paths from the player's initial spawn point acting as a centre for the village.
- After Penusha wrote functions to build the paths and sub-paths, I modified the functions to check for trees and remove them if found.
- Also modified the code to include set air blocks before the path is built to ensure any remnants of wood, sticks etc is eliminated. 
- Modified the path laying functions so that if the path finishes on water, it will continue building for an extra 10 units or when the block beneath is no longer water, whichever comes first.
- Wrote a function to connect the path to the main doors of the house, calling previously written path functions to build the path in the direction required. 
- In the decoration file, wrote lamp post function. This is called in the village file to add a lamp to the middle of the main paths.

Sarang Kuniyil: 25%
- Did initial teraforming blasting the land with air
- trying various methods to make the terraforming blend in with its surroundings.
- made functions to get the maximum height and average height
- made the house on a flush grass ground
- accepted the x and z coordinates of the path so that path is not broken
- created a large enough area for the house and the decorations surronding it 

# GitHub usernames/authors and the corresponding students
s3948240    -  Aayushi Khatri   
AkshitaAgr  -  Akshita Agrawal   
Penusha     -  Penusha Udapamunuwa   
SarangRMIT  -  Sarang Kuniyil   

# Links to the video of the village
- Please log in with your RMIT credentials to view the video as it is shared on the university OneDrive.
    - https://rmiteduau-my.sharepoint.com/:v:/g/personal/s3948240_student_rmit_edu_au/EcsLFkgXiSJEj3SQ409lt6QBsLbUdV5gpilYg7B_yFkthQ?e=XHaXta

- Link to the youtube video
    - https://youtu.be/LHUyFsF-8i0

# Notes
- There are three path files in the final repo of the project. These were left here to show the progression of the path building code. 
- 'path_v2.py' documents the common starting point between Penusha and Aayushi's code.
- 'path_v1.py' documents how Aayushi tried to code the path network. 
- Both of these files were abandoned because Penusha's approach worked better. The final modifications made to the path file by Aayushi resulted in the path building code becoming complete. This combined effort can be found in the 'path.py' file. This is the final version of the file used in the minecraft villages. 
