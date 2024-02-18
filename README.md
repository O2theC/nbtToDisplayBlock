# nbtToDisplayBlock
creates datapacks that create a replicate of a structure from a .nbt using display blocks

# External Library
I use nbt - https://pypi.org/project/NBT/
and pysimplegui - https://pypi.org/project/PySimpleGUI/
it seems pysimplegui has released a 5.0 version that requires dev keys and such, and even with it being free to sign up, I am not a fan of it, I highly reccomend using version 4.60.5 which is the last before version 5.0.0

# Use
download the .py file or the .exe (if you don't know what to do then just get the .exe)
run the file
a gui should pop up, there are a few fields
2 path inputs
2 number inputs
a button named convert
a progress bar
and a exit button

the 2 path inputs are for the .nbt file and the folder where the datapack should go
they should be labeled, use the buttons next to them to open up a file or folder dialog to easy select the file or folder
.nbt are what minecraft uses to store structures, you can find them in the minecraft.jar file or create them using structure blocks
the datapack folder is a folder in every save/world folder and holds datapacks for that save/world

whenever i say that the blocks are placed, they aren't really placed since it's block displays but rather spawned/summoned but placed sounds better rn

the 2 number inputs are for how many blocks should be placed per tick, if the tick count (right box) is 0 then it will place them all at once, if it is more than 1 then it places them based on that delay (NOTE: right now when using a delay, it places the blocks relative to 0 88 0, i have a few ideas on how to fix but i wanted to get this out first), the left box is how many blocks it should place at a time, again if the delay is 0 then it will place all the blocks instantly

press the convert button when your ready to create the datapack, if there are any problems, such as letters in number areas or paths are invaild then a pop up will... pop up, and supply the warning and it will stop and not convert  

the progress bar is a simple way to see how far the script is in making the datapack from the .nbt file


# Why
so for why i made this, 
 - it's cool
 - i got kind of inspired from a Knarfy video , https://www.youtube.com/watch?v=YMooN4S5m6I&pp=ygUGa25hcmZ5 , i saw him having make an entire village house, by hand with block displays (with axiom thankfully) and i made this script to make that kind of stuff easyer
it may not adjust size or anything for inputs but axoim can take care of that
 - i get to mess around in python some more

# Credits
- Knarfy for inspiration / motivation for project idea - this video https://www.youtube.com/watch?v=YMooN4S5m6I&pp=ygUGa25hcmZ5
- PySimpleGUI - amazing library and what i used for the GUI
- nbt library - couldn't read the .nbt files otherwise
- PyInstaller for exe version
