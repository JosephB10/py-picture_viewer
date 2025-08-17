Screenshotting Contraption Thing

Originally Designed because I couldn't see what poker hands were at the end of each round.
I tried making it with OpenCSV2 library but it was struggling with handling the keyboard module.
Which I needed so that I could execute commands even if the picture window wasn't focused.

`
Program Flow -> Greenshot is set up with 2 active shortcuts that are...
- `ctrl alt shift i` to take an image of a custom region.
- `ctrl alt shift o` to take an image of that same region again

These macro's are set to my G6 and G5 Keys with the Logitech Gaming Software for the Logitech G710+.
- So with G5 it lets me select a region to take pictures of
- And G6 retakes the picture of that region instantly

Then my Python script also is looking out for the same G6 Macro of `ctrl alt shift o`.
The script when exectued loops in the pictures folder waiting first for listdir to find the picture and Then
for pygame to successfully be able to load the file. Then you can scroll or use arrow keys to go back and forth 
through the pictures in the folder. Escape to exit.

Backspace will be used to delete the picture you are currently looking at. Delete will delete all the pictures in the folder.
I also need to fix it so that os.listdir sorts the array so that the last picture taken is the last picture. I think I'll
loop through the array, turn each name into a int, and then use that to sort it somehow.