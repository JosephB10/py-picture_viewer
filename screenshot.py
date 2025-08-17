import pygame
from pathlib import Path
import os
import keyboard
import time
import send2trash

def scroll_up():
    global current_image_index

    if (current_image_index < picture_array_cap):
        current_image_index += 1
        update_picture(picture_folder / pictures_array[current_image_index])


def scroll_down():
    global current_image_index

    if (current_image_index > 0):
        current_image_index -= 1
        update_picture(picture_folder / pictures_array[current_image_index])




def delete_photo():
    global pictures_array, current_image_index, picture_array_cap

    print('delete photo')
    send2trash.send2trash(picture_folder / pictures_array[current_image_index])

    #Remove it from list
    pictures_array.pop(current_image_index)

    #reduce the cap
    picture_array_cap -= 1

    scroll_down()


def delete_all_photos():
    global pictures_array, current_image_index, picture_array_cap

    print("DELETE ALL")
    for picture in pictures_array:
        send2trash.send2trash(picture_folder / picture)

    pictures_array = []
    current_image_index = 0
    picture_array_cap = 0
    get_pictures()


def on_hotkey():
    
    old_picture_amount = len(pictures_array)

    #Loop until picture is added to dir, then update
    i = 0
    while True:

        #Make sure it doesn't run forever
        if i > 500:
            print('Didnt find new picture')
            break
        
        #Get all pictures
        new_pictures_array = os.listdir(picture_folder)

        #Check if there is more files now
        if old_picture_amount != len(new_pictures_array):
            get_pictures()
            break
        
        time.sleep(0.1)
        i += 1


def sort_pictures_array():
    global pictures_array

    sorted_files = sorted(pictures_array, key=lambda x: int(x.split(".")[0]))
    print(f'(sorted: {sorted_files}')
    pictures_array = sorted_files



def get_pictures():
    global pictures_array, picture_array_cap, current_image_index

    pictures_array = os.listdir(picture_folder)

    sort_pictures_array()

    picture_array_cap = len(pictures_array) - 1
    current_image_index = picture_array_cap

    #Either use the picture folder if there's pictures or use the default image
    if len(pictures_array) > 0:

        #Loop until the picture is ready to open or we timeout
        count = 0
        while True:
            print("Trying Picture")
            if (count > 500):
                print("Couldn't load picture after 500 tries")
                return

            if (update_picture(picture_folder / pictures_array[current_image_index])):
                print("Picture Up")
                return
            else:
                time.sleep(0.1)
                count += 1

            
    else:
        update_picture(script_path.parent / 'startupImage.jpg')



def update_picture(picturePath):
    try:
        image = pygame.image.load(picturePath)
        screen.blit(image, (0,0))
        pygame.display.flip()
        return True
    except FileNotFoundError:
        print("File not ready")
        return False



# Entry-----------------------------------------------------------------------------------------------------------


#Get the Relative File path
script_path = Path(__file__).resolve()
picture_folder = script_path.parent / 'pictures'


#Globals
first_picture = ""
picture_array_cap = 0
current_image_index = 0
pictures_array = []


keyboard.add_hotkey("ctrl+alt+shift+o", on_hotkey)



#pygame.init()
#Was running into issues with joystick, and all we need is display

pygame.display.init()


#Values
x = 1300
y = 750
fps = 15



screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('image')
clock = pygame.time.Clock()

get_pictures()


#Primary Loop--------------------------------------------------------------------------------------------
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():

        #QUIT
        if event.type == pygame.QUIT:
            running = False

        #MOUSE
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #Scroll up
                scroll_up()
            elif event.button == 5: #Scroll down
                scroll_down()
            elif event.button == 1: #Left Mouse Down
                get_pictures()

        if event.type == pygame.KEYDOWN:
            if event.scancode == 79:  #Right Arrow
                scroll_up()
            if event.scancode == 80: #Left arrow
                scroll_down()
            if event.scancode == 42: #Backspace
                delete_photo()
            if event.scancode == 76: #Delete
                delete_all_photos()
            if event.scancode == 41: #Escape
                running = False
            

pygame.quit()