#Lets make a maze based horror game and open source and and COOL STUFF! :D
#TO DO:
#1 Title screen - Update to be pixel art like wolfenstein - Can't change text alpha - make sure the screen is reseting - We got everything now except the tile being mid and the background - Need opening art and sound
#2D  Sound effects and abeience. Grass walking, timer ticking down, random thunderstorms, rain, enemy being farmer with axe based on the sentry  - Make sure the unload sound stuff is outside game loop lol LETS GOOOO! - Broke immedtieally
#3D Enemy - We have a plan on what we want to do. - It moves hits a wall then stops??? - His code wasn't what we wanted anyway so lets just do our own ig - Used our own its crappy but it works - Make it change states, sprite, etc
#4D  Collectibles keys(the hardest thing probably) - Not even close just follow the turtorial for the exit - Done
#5D  Rain - Should be simple - We can spawn them in but they don't move down or right - Flip rain - Somehow harder than everything else lol - It is done i forgor how we did it
#6  Upload it to the web so others can play - Followed the turtorial didnt work try again. Also sound doesnt even fking work so just make it an executable - take two
#7D Timer - Even closes the game and everything
#8D  2DTextures - Hard as st holy fk back to the drawing board - Really need this working - FINALLY the grounds working but the cubes aint lol - Donne
#9  3D Model - Havent even started lol end me - A key (maybe multiple) and a monster design with two states, ghost sheet and nightmare feul
#10 Hud like wolfenstein - Were doing shoot
#Ideas:
#Maybe have the moon get bigger and bigger after each level idk, red sky too - Nah only one map should have it

#Were changing the game. Now its about you and a freind hunting each other or against an ai. In a hedge mazeD, school, hellD, windows screen saverD, wolfenstein castle, etc
#Each new location is worse and worse for the player
#New TO DO:
#1  Add local splitscreen against a player or against an ai - splitscreen wontwork with the offical texture example - okay now the google ai one inst working - lol we werent starting and ending 3D mode
#2  Add online against u and a freind
#3D  Create a teaser trailer 
#4D Give the player a box for collison - Easy
#5D  Add collison to player and keys and entity - FINALLY just had to master the turtorial lol https://www.raylib.com/examples/models/loader.html?name=models_box_collisions - now on to keys - that is done but it was lazy
#We got the brick texture from here https://www.reddit.com/r/PixelArt/comments/rrjmvl/simple_32x32_brick_wall_pattern_im_gonna_go/
#6D  Make it so that wehenever the map changes the keys location change too - just had to make it a function wasnt too hard honestly
#7  Add models to the keysD, player and chaser entity
#8  Add new ways to move camera for no mouse people 
#Lore:
#You've been invited to inside a house, then a basement thats flooded, a maze in the pouring rain, then other places


#Import
import pyray as pr
import math
import random
import asyncio
#Mixer
import pygame as pg
pg.init()
pg.mixer.init()
# make channels
cnl_1 = pg.mixer.Channel(0) # Background or one time music
cnl_2 = pg.mixer.Channel(1) # Player footsteps
cnl_3  = pg.mixer.Channel(2) # Enemy noises
cnl_4 = pg.mixer.Channel(3) # Extra


async def main():
    pr.init_window(800, 600, "Hunted")
    pr.init_audio_device()
    map = 0
    local = 0 #0 is against ai or online and 1 is agianst freind
    pr.rl_set_line_width(3) #this even important
    #Sounds
    # one time sound effect
    thunder_se = pg.mixer.Sound("sound/open_thunder.ogg") 
    thunder_se.set_volume(0.8)
    thunder_played = False
    rain_msc = pg.mixer.Sound("sound/rain.ogg") 
    rain_msc.set_volume(0.5)
    fsteps_se = pg.mixer.Sound("sound/grass_walk.ogg") 
    fsteps_se.set_volume(0.2)
    tick_se = pg.mixer.Sound("sound/clock_tick.ogg") 
    tick_se.set_volume(0.1)
    # long time music
    chase_msc = pg.mixer.Sound("sound/mr.edmund_chasing.mp3") 
    chase_msc.set_volume(0.8)
    #Classes and Objects
    player_1 = Player("runner", local)
    maze = Maze()
    maze.set_keys()
    if (local == 0):
        enemy = other("ai")
    if (local == 1):
        enemy = other("player")
    #Rain logic
    rains = []
    rain_cc = 0
    rain_add_inc = 50
    new_rain = Rain()
    rains.append(new_rain)
    if (map == 1):
        for i in range(100):
            new_rain = Rain()
            new_rain.pos.y = random.randint(-10, pr.get_screen_height())
            rains.append(new_rain)
    #Load the texture
    # floor
    floor_mesh = pr.gen_mesh_plane(maze.size, maze.size, 1, 1)
    floor_model = pr.load_model_from_mesh(floor_mesh)
    floor_texture = pr.load_texture("assests/floor_wood.jpeg")
    floor_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = floor_texture
    # walls
    cube_mesh = pr.gen_mesh_cube(1, 1.5, 1)
    cube_model = pr.load_model_from_mesh(cube_mesh)
    cube_texture = pr.load_texture("assests/wood.jpeg")
    cube_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = cube_texture
    #Title
    game_state = "title"
    title_part = 0
    # part 1
    pt_1_a = 1.0
    pt_1_col = pr.fade(pr.WHITE, pt_1_a)
    # part 2
    pt_2_a = 1.0
    pt_2_col = pr.fade(pr.WHITE, pt_1_a)
    #Timer
    timer = 60
    time_add_inc = 1000 #this one goes faster when map is in the brick maze for some reason (our geuss was that the game was saving memory as the other rain timer wasnt happening) - who cares
    time_cc = 0
    time_col = pr.WHITE
    #Keys
    keys_got = 0
    # to keep track of which key we hit and didnt
    key1_y, key2_y, key3_y = 0.2, 0.2, 0.2
    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        #Fullscreen
        if pr.is_key_pressed(pr.KEY_F):
            pr.toggle_fullscreen()
        #Title screen
        if (game_state == "title"):
            if (title_part == 0):   
                #Fade text animation
                pt_1_col = pr.fade(pr.WHITE, pt_1_a)
                pt_1_a -= 0.10 * pr.get_frame_time()
                pr.draw_text(f"PyGuy Presents", 10, pr.get_screen_height() - 50, 30, pt_1_col)
                #print(pt_1_a)
                #Next part
                if (pt_1_a <= 0.5):
                    title_part = 2
            #Go to title screen skip
            if (pr.is_key_down(pr.KEY_ENTER)):
                title_part = 2
                pt_2_a = 0
            if (title_part == 2): 
                if (map == 1):
                    #Rain
                    rain_cc += 1
                    if (rain_cc > rain_add_inc):
                        new_rain = Rain()
                        rains.append(new_rain)
                        rain_cc = 0
                    for r in rains:
                        r.update()
                #Thunder animation
                pt_2_col = pr.fade(pr.WHITE, pt_2_a)
                pt_2_a -= 0.35 * pr.get_frame_time()
                pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pt_2_col); 
                #Sound - Thunder
                if not (thunder_played):
                    cnl_1.play(thunder_se)
                    thunder_played = True
                # Words
                pr.draw_text(f"Hunted", 20, 100, 40, pr.WHITE)
                pr.draw_text(f"1 Local", 20, 150, 30, pr.WHITE)
                pr.draw_text(f"2 Online", 20, 190, 30, pr.WHITE)
                # Change menu to local
                if (pr.is_key_down(pr.KEY_ONE)):
                    title_part = 3
                # Change menu to local
                if (pr.is_key_down(pr.KEY_TWO)):
                    title_part = 4
            #Local title menu
            if (title_part == 3):
                # Title
                pr.draw_text(f"Local", int(pr.get_screen_width()/2) - 100, 20, 100, pr.WHITE)
                # Words
                pr.draw_text(f"3 Ai", 20, 150, 30, pr.WHITE)
                pr.draw_text(f"4 Co-Op", 20, 190, 30, pr.WHITE)
                pr.draw_text(f"5 Back", 20, 230, 30, pr.WHITE)
                # AI
                if (pr.is_key_down(pr.KEY_THREE)):
                    local = 0
                    #Setup camera
                    camera_1 = pr.Camera3D((0, 0.5, 0), (1, 0.5, 1), (0, 1, 0), 100, pr.CAMERA_PERSPECTIVE) #Dont ever changee the last one bro
                    game_state = "play"
                    player_1.hud(keys_got, timer, time_col, local)
                # Splitscreen
                if (pr.is_key_down(pr.KEY_FOUR)):
                    local = 1
                    #Setup cameras
                    split_1 = pr.Rectangle(int(0), int(0), int(pr.get_screen_width()/2.0), int(pr.get_screen_height()))
                    camera_1 = pr.Camera3D((0, 0.5, 0), (1, 0.5, 1), (0, 1, 0), 45, pr.CAMERA_PERSPECTIVE)
                    split_2 = pr.Rectangle(int(pr.get_screen_width()/2.0), int(0), int(pr.get_screen_width()/2.0), int(pr.get_screen_height()))
                    camera_2 = pr.Camera3D((0, 1, 0), (1, 1, 0), (1, 1, 1), 45, pr.CAMERA_PERSPECTIVE)
                    player_1.hud(keys_got, timer, time_col, local) #needs to be here for some reason - still not working
                    game_state = "play"
                # Go back
                if (pr.is_key_down(pr.KEY_FIVE)):
                    title_part =2
            #Online title menu
            if (title_part == 4):
                # Title
                pr.draw_text(f"Online", int(pr.get_screen_width()/2) - 150, 20, 100, pr.WHITE)
                pr.draw_text(f"5 Back", 20, 150, 30, pr.WHITE)
                # Go back
                if (pr.is_key_down(pr.KEY_FIVE)):
                    title_part = 5

        #Game
        if (game_state == "play"):
            #Sky 
            if (map == 0): #House
                pr.clear_background(pr.DARKBROWN)
            if (map == 1): #Basement
                pr.clear_background(pr.LIGHTGRAY)
            if (map == 2): #Outside maze
                pr.clear_background(pr.BLACK)
            if (map == 3): #Hell (temp)
                pr.clear_background(pr.RED)
            #Effects
            #UI
            # Timer
            time_cc += 1
            if (time_cc >= time_add_inc):
                timer -= 1
                time_cc = 0
                cnl_2.play(tick_se)
            #  Colors
            if (timer <= 30 and timer >= 15):
                time_col = pr.YELLOW
                tick_se.set_volume(0.4)
                #time_add_inc = 1500
            if (timer <= 14):
                time_col = pr.RED
                tick_se.set_volume(0.5)
                #time_add_inc = 500
            #Draw stuff
            pr.begin_mode_3d(camera_1)
            #Specific map stuff
            # Moon
            if (map == 2): 
                pr.draw_sphere(pr.Vector3(10, 50, 5), 2, pr.Color(250, 250, 250, 255))
            #World
            #pr.draw_grid(maze.size*10, 0) #adjust last variable by decimals for borders on ground
            # Floor - Both texure and no texture
            if (map == 0): #House
                #pr.draw_plane((0, 0.01, 0), (maze.size*2, maze.size*2), pr.DARKBROWN)
                pr.draw_model(floor_model, (7, 0.01, 7), 1.0, pr.DARKBROWN)
            if (map == 1): #Basement
                pr.draw_plane((0, -0.01, 0), (maze.size*2, maze.size*2), pr.DARKBLUE)
            if (map == 2): #Outside maze
                pr.draw_model(floor_model, (0, 0.01, 0), 1.0, pr.DARKGREEN)
            if (map == 3): #Hell (temp)
                pr.draw_model(floor_model, (1, 0.01, 1), 1.0, pr.RED) # floor wasnt showing cause of a y issue
            #Other (thing, player, ai)
            enemy.update(player_1, chase_msc)
            #Sound Effects
            # cnl_4.play(rain_msc)
            #Draw maze - i is x j is z so if you want to make a wireframe do that
            for i in range(maze.size):
                for j in range(maze.size):
                    if (maze.maze[i][j] != 0):
                        #Walls - Texture, cube and color tint
                        if (map == 0): #House
                            pr.draw_cube((i+0.5, 0.5, j + 0.5), 1, 1.5, 1, pr.BROWN) #maze.colors[i][j])
                            pr.draw_model(cube_model, (i + 0.5, 0.5, j + 0.5), 1.1, pr.BROWN)
                        if (map == 1): #Basement
                            pr.draw_cube((i+0.5, 0.5, j + 0.5), 1, 1.5, 1, pr.WHITE)
                            pr.draw_model(cube_model, (i + 0.5, 0.5, j + 0.5), 1.1, pr.WHITE)
                        if (map == 2): #Outside maze
                            pr.draw_cube((i+0.5, 0.5, j + 0.5), 1, 1.5, 1, pr.GREEN)
                            pr.draw_model(cube_model, (i + 0.5, 0.5, j + 0.5), 1.1, pr.GREEN)
                        if (map == 3): #Hell (temp)
                            pr.draw_cube((i+0.5, 0.5, j + 0.5), 1, 1.5, 1, pr.RED)
                            pr.draw_model(cube_model, (i + 0.5, 0.5, j + 0.5), 1.1, pr.RED)
                        # Wall Shaders
                        pr.draw_cube((i+0.502, 0.5 - 0.002, j + 0.502), 1, 1, 1, (0, 0, 0, 100))
                        pr.draw_cube((i+0.503, 0.5  - 0.003, j + 0.498), 1, 1, 1, (0, 0, 0, 50))
                        # Floor shaders
                        pr.draw_plane((i + 1, 0.02, j + 0.5), (0.7, 1), (0, 0, 0, 100))
                        #Keys
                        # Player collison with keys
                        if ((pr.check_collision_boxes(pr.BoundingBox(pr.Vector3(player_1.pos.x -  player_1.size.x/2,  player_1.pos.y -  player_1.size.y/2,  player_1.pos.z -  player_1.size.z),
                                                        pr.Vector3(player_1.pos.x +  player_1.size.x/2,  player_1.pos.y +  player_1.size.y/2,  player_1.pos.z + player_1.size.z/2)),
                                        pr.BoundingBox(pr.Vector3(maze.key_1[0] + 0.5 - 0.5/2, key1_y - 0.5/2, maze.key_1[1] + 0.5 - 0.5/2),
                                                        pr.Vector3(maze.key_1[0] + 0.5 + 0.5/2, key1_y + 0.5/2, maze.key_1[1] + 0.5 + 0.5/2))))):
                            keys_got += 1
                            key1_y = -200
                        if ((pr.check_collision_boxes(pr.BoundingBox(pr.Vector3(player_1.pos.x -  player_1.size.x/2,  player_1.pos.y -  player_1.size.y/2,  player_1.pos.z -  player_1.size.z),
                                                        pr.Vector3(player_1.pos.x +  player_1.size.x/2,  player_1.pos.y +  player_1.size.y/2,  player_1.pos.z + player_1.size.z/2)),
                                        pr.BoundingBox(pr.Vector3(maze.key_2[0] + 0.5 - 0.5/2, key2_y - 0.5/2, maze.key_2[1] + 0.5 - 0.5/2),
                                                        pr.Vector3(maze.key_2[0] + 0.5 + 0.5/2, key2_y + 0.5/2, maze.key_2[1] + 0.5 + 0.5/2))))):
                            keys_got += 1
                            key2_y = -200
                        if ((pr.check_collision_boxes(pr.BoundingBox(pr.Vector3(player_1.pos.x -  player_1.size.x/2,  player_1.pos.y -  player_1.size.y/2,  player_1.pos.z -  player_1.size.z),
                                                        pr.Vector3(player_1.pos.x +  player_1.size.x/2,  player_1.pos.y +  player_1.size.y/2,  player_1.pos.z + player_1.size.z/2)),
                                        pr.BoundingBox(pr.Vector3(maze.key_3[0] + 0.5 - 0.5/2, key3_y - 0.5/2, maze.key_3[1] + 0.5 - 0.5/2),
                                                        pr.Vector3(maze.key_3[0] + 0.5 + 0.5/2, key3_y + 0.5/2, maze.key_3[1] + 0.5 + 0.5/2))))):
                            keys_got += 1
                            key3_y = -200
                        # Draw keys
                        #pr.draw_cube((maze.key_1[0] + 0.5, key1_y, maze.key_1[1]+0.5), 0.5, 0.5, 0.5, pr.YELLOW) # hitbox
                        # Actual key
                        pr.draw_cube((maze.key_1[0] + 0.5, key1_y + 0.3, maze.key_1[1]+0.5), 0.3, 0.3, 0.3, pr.YELLOW)
                        pr.draw_cube((maze.key_1[0] + 0.5, key1_y, maze.key_1[1]+0.5), 0.2, 0.4, 0.2, pr.YELLOW)
                        #pr.draw_cube((maze.key_2[0] + 0.5, key2_y, maze.key_2[1]+0.5), 0.5, 0.5, 0.5, pr.YELLOW) # hitbox
                        # Actual key
                        pr.draw_cube((maze.key_2[0] + 0.5, key2_y + 0.3, maze.key_2[1]+0.5), 0.3, 0.3, 0.3, pr.YELLOW)
                        pr.draw_cube((maze.key_2[0] + 0.5, key2_y, maze.key_2[1]+0.5), 0.2, 0.4, 0.2, pr.YELLOW)
                        #pr.draw_cube((maze.key_3[0] + 0.5, key3_y, maze.key_3[1]+0.5), 0.5, 0.5, 0.5, pr.YELLOW) # hitbox
                        # Actual key
                        pr.draw_cube((maze.key_3[0] + 0.5, key3_y + 0.3, maze.key_3[1]+0.5), 0.3, 0.3, 0.3, pr.YELLOW)
                        pr.draw_cube((maze.key_3[0] + 0.5, key3_y, maze.key_3[1]+0.5), 0.2, 0.4, 0.2, pr.YELLOW)
            #Next level
            if (keys_got == 3): # Testing has it at 1 og is 3
                map += 1
                # Change texture to Brick
                if (map == 1):
                    # walls
                    cube_mesh = pr.gen_mesh_cube(1, 1.5, 1)
                    cube_model = pr.load_model_from_mesh(cube_mesh)
                    cube_texture = pr.load_texture("assests/brick.jpg")
                    cube_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = cube_texture
                # Change texture to Hedge
                if (map == 2):
                    # floor
                    floor_mesh = pr.gen_mesh_plane(maze.size*2, maze.size*2, 1, 1)
                    floor_model = pr.load_model_from_mesh(floor_mesh)
                    floor_texture = pr.load_texture("assests/grass.png")
                    floor_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = floor_texture
                    # walls
                    cube_mesh = pr.gen_mesh_cube(1, 1.5, 1)
                    cube_model = pr.load_model_from_mesh(cube_mesh)
                    cube_texture = pr.load_texture("assests/hedges.jpeg")
                    cube_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = cube_texture
                # Change texture to Flesh
                if (map == 3):
                    # floor
                    floor_mesh = pr.gen_mesh_plane(maze.size*2, maze.size*2, 1, 1)
                    floor_model = pr.load_model_from_mesh(floor_mesh)
                    floor_texture = pr.load_texture("assests/muscle.jpg")
                    floor_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = floor_texture
                    # walls
                    cube_mesh = pr.gen_mesh_cube(1, 1.5, 1)
                    cube_model = pr.load_model_from_mesh(cube_mesh)
                    cube_texture = pr.load_texture("assests/wallofflesh.jpeg")
                    cube_model.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = cube_texture
                #Reset values
                keys_got = 0
                key1_y, key2_y, key3_y = 0.2, 0.2, 0.2
                player_1.pos = pr.Vector3(1.5, 0.7, 1.5)
                enemy.pos =  pr.Vector3(13, 0.3, 13)
                timer = 60
                other.mode = "finding"
                maze.set_keys()

            #Player update
            player_1.update(enemy)
            #Other Entity
            pr.draw_cube(enemy.pos, enemy.size.x, enemy.size.y, enemy.size.z ,pr.fade(pr.WHITE, 0.2)) # changed from caspule for better collison
            #Close
            if (timer <= 0):
                pr.close_window()
            pr.end_mode_3d()

            # Local is false
            if (local == 0):
                pr.begin_mode_3d(camera_1)
                #Camera
                player_1.controls(maze)
                #Key collison
                    #player = Player()
                    #maze = Maze(level*2+15) #increase size of maze"""
                camera_1.position = player_1.pos
                camera_1.target = pr.vector3_add(player_1.pos, player_1.dir) #only camera 1 moves camera through mouse need to add camera 2 moving through keys
                #2D stuff being overlayed
                pr.end_mode_3d()    
                # Hud
                player_1.hud(keys_got, timer, time_col, local) 
                #Rain
                # spawn rain
                if (map == 2):
                    rain_cc += 1
                    if (rain_cc > rain_add_inc):
                        new_rain = Rain()
                        rains.append(new_rain)
                        rain_cc = 0
                    for r in rains:
                        r.update()
                #Brightness
                if (map == 2) or (map == 3):
                    pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.fade(pr.BLACK, 0.5))
                if (map == 1):
                    pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.fade(pr.BLACK, 0.3))

            # Local is True
            if (local == 1):
                # Player 1 "runner"
                pr.begin_scissor_mode(int(split_1.x), int(split_1.y), int(split_1.width), int(split_1.height))
                pr.begin_mode_3d(camera_1)
                player_1.controls(maze)
                camera_1.position = player_1.pos
                camera_1.target = pr.vector3_add(player_1.pos, player_1.dir) #only camera 1 moves camera through mouse need to add camera 2 moving through keys
                pr.end_mode_3d()
                #2D stuff being overlayed
                # Hud
                player_1.hud(keys_got, timer, time_col, local) 
                #Rain
                # spawn rain
                if (map == 2):
                    rain_cc += 1
                    if (rain_cc > rain_add_inc):
                        new_rain = Rain()
                        rains.append(new_rain)
                        rain_cc = 0
                    for r in rains:
                        r.update()
                #Brightness
                if (map == 2) or (map == 3):
                    pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.fade(pr.BLACK, 0.5))
                if (map == 1):
                    pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.fade(pr.BLACK, 0.3))
                # Player 2 "chaser"
                pr.begin_scissor_mode(int(split_2.x), int(split_2.y), int(split_2.width), int(split_2.height))
                pr.begin_mode_3d(camera_2)
                #Move camera
                camera_2.position = enemy.pos
                camera_2.target = pr.vector3_add(enemy.pos, pr.Vector3(3, 5, 0))
                pr.end_mode_3d()

                #End scissoring (hahaha) screen 
                pr.end_scissor_mode()

        pr.end_drawing()
        await asyncio.sleep(0)

    #Exit game
    else:
        # Reset window if fullscreen
        if (pr.is_window_fullscreen()):
            pr.toggle_fullscreen() # Exit fullscreen
            pr.set_window_size(1920, 1080); # Reset to desired default resolution


#Classes
class Rain():
    def __init__(self):
        self.pos = pr.Vector2(random.randint(-50, pr.get_screen_width()), -10)
        self.speed = 100

    def move(self):
        self.pos.x += self.speed/2 * pr.get_frame_time()
        self.pos.y += self.speed * pr.get_frame_time() * 2

    def update(self):
        self.move()
        pr.draw_line(int(self.pos.x), int(self.pos.y), int(self.pos.x + 5), int(self.pos.y + 5), pr.SKYBLUE)


class Player():
    def __init__(self, id, local):
        self.id = id
        self.local = local
        self.pos = pr.Vector3(1.5, 0.7, 1.5) #OG: 1.5, 0.7, 1.5
        self.yaw = 0
        self.pitch = 0
        self.sensetivity = 0.003
        self.dir = pr.Vector3(1, 0, 1)
        self.speed = 2
        self.size = pr.Vector3(0.2, 0.5, 0.2)
        #Health
        self.hearts = []
        self.can_be_hurt = True
        self.hurt_add_inc = 500
        self.hurt_cc = 0 
        if (local == 0):
            self.ht_x = int(pr.get_screen_width()/2 - 100)
        else:
            self.ht_x = int(pr.get_screen_width()/2 - 260)
        self.made_hearts = False
        pr.disable_cursor()
    
    def controls(self, maze):
            speed = pr.get_frame_time() * self.speed
            #Mouse
            mouse_delta = pr.get_mouse_delta() #location of mouse
            self.yaw -= mouse_delta.x * self.sensetivity 
            self.pitch = max(-1.57, min(1.57, self.pitch - mouse_delta.y * self.sensetivity))
            sin_yaw, cos_yaw = math.sin(self.yaw), math.cos(self.yaw)
            #adjust cam dir
            self.dir.x = math.cos(self.pitch) * sin_yaw
            self.dir.y = math.sin(self.pitch)
            self.dir.z = math.cos(self.pitch) * cos_yaw
            # Movement - they did the cool thing where you subtract different key spaces
            forward = pr.is_key_down(pr.KEY_W) - pr.is_key_down(pr.KEY_S)
            sideward = pr.is_key_down(pr.KEY_D) - pr.is_key_down(pr.KEY_A)

            if (forward != 0 and sideward != 0):
                speed *= 0.707
            #Just the x and z nothing too serious
            nx, nz = self.pos.x, self.pos.z
            nx += speed * (sin_yaw * forward - cos_yaw * sideward)
            nz += speed * (cos_yaw * forward + sin_yaw * sideward)
            #Collison
            # walls
            if (maze.p_no_collison(nx, nz)):
                self.pos.x, self.pos.z = nx, nz
            elif (maze.p_no_collison(nx, self.pos.z)):
                self.pos.x = nx
            if (maze.p_no_collison(self.pos.x, nz)):
                self.pos.z = nz
    
    def damage(self):
        if (self.can_be_hurt == False):
            self.hurt_cc += 1
            if (self.hurt_cc >= self.hurt_add_inc):
                self.hurt_cc = 0
                self.can_be_hurt = True

    def hud(self, keys_got, timer, time_col, local):
        if (local == 0):
            if (self.made_hearts == False):
                self.ht_x = int(pr.get_screen_width()/2 - 100)
                # make hearts - Had to move so much shit just to get the fking hearts working in co op 
                for i in range (3):
                    new_heart = pr.Rectangle(self.ht_x, int(pr.get_screen_height() - 75), 40, 40)
                    self.ht_x += 70
                    self.hearts.append(new_heart)
                self.made_hearts = True
            #Box
            main_base = pr.Rectangle(int(pr.get_screen_width()/2 - 250), int(pr.get_screen_height() - 105), 500, 85)
            pr.draw_rectangle(int(main_base.x), int(main_base.y), int(main_base.width), int(main_base.height), pr.LIGHTGRAY)
            #Timer
            # text
            pr.draw_text(f"Time Left:",int(main_base.x + 15), int(main_base.y + 10), 20, time_col)
            # amount 
            pr.draw_text(f"{timer}",int(main_base.x + 20), int(main_base.y + 30), 50, time_col)
            # seperating line
            pr.draw_line(int(main_base.x + 125), int(main_base.y), int(main_base.x + 125), int(main_base.y + main_base.height), pr.DARKGRAY)
            #Hearts
            # objects
            for ht in self.hearts:
                pr.draw_rectangle(int(ht.x), int(ht.y), int(ht.width), int(ht.height), pr.RED)
            # text
            pr.draw_text(f"Health",int(main_base.x + main_base.width/2 - 40), int(main_base.y + 10), 20, pr.RED)
            #Keys
            # text 
            pr.draw_text(f"Keys {keys_got}", int(main_base.x + main_base.width - 125), int(main_base.y + 10), 20, pr.YELLOW)
            # seperating line
            pr.draw_line(int(main_base.x + 370), int(main_base.y), int(main_base.x + 370), int(main_base.y + main_base.height), pr.DARKGRAY)
            #Box outline
            pr.draw_rectangle_lines_ex(main_base, 10, pr.DARKGRAY)
        if (local == 1):
            if (self.made_hearts == False):
                self.ht_x = int(pr.get_screen_width()/2 - 260)  #Had to move so much shit just to get the fking hearts working in co op FK
                # make hearts
                for i in range (3):
                    new_heart = pr.Rectangle(self.ht_x, int(pr.get_screen_height() - 75), 40, 40)
                    self.ht_x += 70
                    self.hearts.append(new_heart)
                self.made_hearts = True
            #Box
            main_base = pr.Rectangle(int(10), int(pr.get_screen_height() - 105), 400, 85)
            pr.draw_rectangle(int(main_base.x), int(main_base.y), int(main_base.width), int(main_base.height), pr.LIGHTGRAY)
            #Timer
            # text
            pr.draw_text(f"Time Left:",int(main_base.x + 15), int(main_base.y + 10), 20, time_col)
            # amount 
            pr.draw_text(f"{timer}",int(main_base.x + 20), int(main_base.y + 30), 50, time_col)
            # seperating line
            pr.draw_line(int(main_base.x + 125), int(main_base.y), int(main_base.x + 125), int(main_base.y + main_base.height), pr.DARKGRAY)
            #Hearts
            # objects
            for ht in self.hearts:
                pr.draw_rectangle(int(ht.x), int(ht.y), int(ht.width), int(ht.height), pr.RED)
            # text
            pr.draw_text(f"Health",int(main_base.x + main_base.width/2 - 10), int(main_base.y + 10), 20, pr.RED)
            #Keys
            # text 
            pr.draw_text(f"Keys {keys_got}", int(main_base.x + main_base.width - 80), int(main_base.y + 10), 20, pr.YELLOW)
            # seperating line
            pr.draw_line(int(main_base.x + 320), int(main_base.y), int(main_base.x + 320), int(main_base.y + main_base.height), pr.DARKGRAY)
            #Box outline
            pr.draw_rectangle_lines_ex(main_base, 10, pr.DARKGRAY)
        #print(local)
        

    def update(self, enemy):
        #Draw
        pr.draw_cube(self.pos, self.size.x, self.size.y, self.size.z, pr.BLUE)
        #Damage
        self.damage()
        #Collison with entity
        if (self.can_be_hurt == True):
            if (pr.check_collision_boxes(pr.BoundingBox(pr.Vector3(self.pos.x - self.size.x/2, self.pos.y - self.size.y/2, self.pos.z - self.size.z),
                                                        pr.Vector3(self.pos.x + self.size.x/2, self.pos.y + self.size.y/2, self.pos.z + self.size.z/2)),
                                        pr.BoundingBox(pr.Vector3(enemy.pos.x - enemy.size.x/2, enemy.pos.y - enemy.size.y/2, enemy.pos.z - enemy.size.z/2),
                                                        pr.Vector3(enemy.pos.x + enemy.size.x/2, enemy.pos.y + enemy.size.y/2, enemy.pos.z + enemy.size.z/2)))):
                self.can_be_hurt = False
                if (len(self.hearts) > 0):
                    self.hearts.pop()
        #Player dies
        if (len(self.hearts) <= 0):
            pr.close_window()
            if (pr.is_window_fullscreen()):
                pr.toggle_fullscreen() # Exit fullscreen
                pr.set_window_size(1920, 1080); # Reset to desired default resolution`


#Turtorial dude stole this somewhere doubt we'll use this in future - Ironic
class Maze():
    def __init__(self, size=15): #what that size do - 
        self.size = size
        self.maze = [[1] * self.size for _ in range(self.size)]
        #Random colors we don't want this (unless we can change it all through textures)
        self.colors = [[[random.randint(0, 255) for _ in range(3)] + 
                        [255] for _ in range(self.size)] for _ in range(self.size)] 
        #self.heights = [[round(round(random.uniform(0.2, 2), 1) for _ in range(self.size))] for _ in range(self.size)] #stuffs annoying
        
        def carve(x, y): #Makes the maze 
            self.maze[x][y] = 0
            dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(dirs)

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.size - 1 and 1 <= ny < self.size -1 and self.maze[nx][ny] == 1):
                    self.maze[x + dx//2][y + dy//2] = 0
                    carve(nx, ny)

        carve(1, 1)
        #What does this do?
        for _ in range(self.size*2):
            self.maze[random.randint(1, self.size-2)][random.randint(1, self.size-2)] = 0
        
    def set_keys(self):
        #Keys - Find a way to draw them better
        self.key_1 = random.randint(1, self.size - 2), random.randint(1, self.size - 2), random.randint(1, self.size - 2)
        self.maze[self.key_1[0]][self.key_1[1]] = 0 # i think this code replaces the maze wall with the key 
        self.key_2 = random.randint(1, self.size - 2), random.randint(1, self.size - 2), random.randint(1, self.size - 2)
        self.maze[self.key_2[0]][self.key_2[1]] = 0
        self.key_3 = random.randint(1, self.size - 2), random.randint(1, self.size - 2), random.randint(1, self.size - 2)
        self.maze[self.key_3[0]][self.key_3[1]] = 0

    #Player
    def p_no_collison(self, nx, nz):
        if (self.maze[int(nx+0.1)][int(nz+0.1)] != 0 or self.maze[int(nx + 0.1)][int(nz)] != 0 or
            self.maze[int(nx)][int(nz + 0.1)] != 0 or self.maze[int(nx - 0.1)][int(nz)] != 0 or 
            self.maze[int(nx)][int(nz - 0.1)] != 0 or self.maze[int(nx - 0.1)][int(nz - 0.1)] != 0):
            return 0
        return 1
    # keys

#He made a guy that runs through the maze we want a CHASER! What if he could phase through the maze...cause hes like a ghost or some shit. YOOOOO!
#The guys code wasnt a random move through it was a set point or whatever so were using ours
#Either its ai or freind
class other():
    def __init__(self, id):
        self.pos = pr.Vector3(13, 0.3, 13)
        self.speed = 0.5
        self.tar_x = random.randrange(1, 13)
        self.tar_z = random.randrange(1, 13)
        self.tar_thres = 0.1
        self.play_thres = 5
        self.mode = "finding"
        self.id = id
        self.size = pr.Vector3(0.5, 2, 0.5)

    def move(self, player, chase):
        if (self.mode == "finding"):
            self.speed = 0.5
            #Moving
            if (self.pos.x < self.tar_x):
                self.pos.x += self.speed * pr.get_frame_time()
            if (self.pos.x > self.tar_x):
                self.pos.x -= self.speed * pr.get_frame_time()
            if (self.pos.z < self.tar_z):
                self.pos.z += self.speed * pr.get_frame_time()
            if (self.pos.z > self.tar_z):
                self.pos.z -= self.speed * pr.get_frame_time()
            #At OR close to target position
            if (abs(self.pos.x - self.tar_x) <= self.tar_thres) and (abs(self.pos.z - self.tar_z) <= self.tar_thres): #this was annoying but here it is
                self.tar_x = random.randrange(1, 13)
                self.tar_z = random.randrange(1, 13)
            #Close to player
            if (abs(self.pos.x - player.pos.x) <= self.play_thres) and (abs(self.pos.z - player.pos.z) <= self.play_thres):
                self.mode = "chasing"

        if (self.mode == "chasing"):
            self.speed = 0.9
            #Moving
            if (self.pos.x < player.pos.x):
                self.pos.x += self.speed * pr.get_frame_time()
            if (self.pos.x > player.pos.x):
                self.pos.x -= self.speed * pr.get_frame_time()
            if (self.pos.z < player.pos.z):
                self.pos.z += self.speed * pr.get_frame_time()
            if (self.pos.z > player.pos.z):
                self.pos.z -= self.speed * pr.get_frame_time()
            #Far from player
            if (abs(self.pos.x - player.pos.x) >= 0.5) and (abs(self.pos.z - player.pos.z) >= 0.5): #its fair but stil tuff
                  self.mode = "finding"

    def update(self, player, chase):
        self.move(player, chase)
        #Collison idk if we want it or not or when we do
        """if (maze.no_collison(nx, self.pos.z)):
            self.pos.x = nx
        if (maze.no_collison(self.pos.x, nz)):
            self.pos.z = nz"""

asyncio.run(main())

