import cv2
from pathlib import Path
import os
import keyboard
import time

def mouse_callback(event, x, y, flags, param):
    global current_image_index

    if event == cv2.EVENT_MOUSEWHEEL and picture_array_cap > 0:
        if(flags > 0):
            if(current_image_index < picture_array_cap):
                current_image_index += 1
                update_picture(picture_folder / pictures_array[current_image_index])
        else: 
            if(current_image_index > 0):
                current_image_index -= 1
                update_picture(picture_folder / pictures_array[current_image_index])

    elif event == cv2.EVENT_LBUTTONUP:
        get_pictures(False)



def update_picture(picture):
    print('update pic')
    #Read the picture into memory
    image = cv2.imread(picture)
    print(picture)
    #Resize picture
    scaled = cv2.resize(image, (1300, 750))

    #Launch the dispaly
    cv2.imshow('opencsvImage', scaled)


def on_hotkey():
    print('hello')
    
    old_picture_amount = len(pictures_array)
    i = 0
    while True:
        print(i)
        if i > 500:
            print('Didnt find new picture')
            break
        
        new_pictures_array = os.listdir(picture_folder)

        if old_picture_amount != len(new_pictures_array):
            print('found new picture')
            time.sleep(5)
            print('get pictures')
            get_pictures(new_pictures_array)
            break
        
        time.sleep(0.1)
        i += 1


def get_pictures(new_pictures_array):
    global pictures_array, picture_array_cap, current_image_index

    if (new_pictures_array):
        pictures_array = new_pictures_array
    else:
        pictures_array = os.listdir(picture_folder)


    print(pictures_array)
    picture_array_cap = len(pictures_array) - 1
    current_image_index = picture_array_cap

    if len(pictures_array) > 0:
        update_picture(picture_folder / pictures_array[current_image_index])
        print(picture_folder / pictures_array[current_image_index])
    else:
        update_picture(script_path.parent / 'startupImage.jpg')



#Get the Relative File path
script_path = Path(__file__).resolve()
picture_folder = script_path.parent / 'pictures'


#Globals
first_picture = ""
picture_array_cap = 0
current_image_index = 0
pictures_array = []



#Get pictures in folder and open the last one
get_pictures(False)

#Capture global keypresses
keyboard.add_hotkey("ctrl+alt+shift+o", on_hotkey)

#Capture mouse actions on window
cv2.setMouseCallback('opencsvImage', mouse_callback)




#Keep program open until esc key, or the window is closed
while True: 
    print (cv2.getWindowProperty("opencsvImage", cv2.WND_PROP_VISIBLE))
    #Loop logic
    key = cv2.waitKey(0)
    time.sleep(0.3)

    #Check for exits
    if (key == 27):
        break

    if (cv2.getWindowProperty("opencsvImage", cv2.WND_PROP_VISIBLE) == 0):  #returns 1 if window open, 0 if window closed
        break

    print('loopy')




cv2.destroyAllWindows()