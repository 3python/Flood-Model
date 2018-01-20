# -*- coding: utf-8 -*-

"""
Created on Tue Dec 19 09:51:56 2017

@author: kate

Citation for using matplotlib
@Article{Hunter:2007,
  Author    = {Hunter, J. D.},
  Title     = {Matplotlib: A 2D graphics environment},
  Journal   = {Computing In Science \& Engineering},
  Volume    = {9},
  Number    = {3},
  Pages     = {90--95},
  abstract  = {Matplotlib is a 2D graphics package used for Python
  for application development, interactive scripting, and
  publication-quality image generation across user
  interfaces and operating systems.},
  publisher = {IEEE COMPUTER SOC},
  doi = {10.1109/MCSE.2007.55},
  year      = 2007
}
"""

#Imports.
import os.path
#Matplotlib plots graphs.
import matplotlib
import matplotlib.pyplot
import matplotlib.animation
matplotlib.use('TkAgg')
import matplotlib.backends.backend_tkagg
#Allows creation of a GUI.
#Importing this way imports all the modules, such as frame and text.
import tkinter
from tkinter import *

#Importing the script that contains the functions to run the model.
import script


#User inputs

#Creating a blank document so that error message will appear if program tries to open
#the file but one has not been entered.
document = ""

#Getting the user to enter what file they would like to use.
document = script.document_input()

#DEM created from opening the height data.
#Works as long as there is a name assigned to the document variable.
if document !="":
    #How to convert the file is has csv extension.
    if (document[-1]) == 'v':
        #Tries to open the file and convert to a double list.
        try:
            dem = script.sesamie(document)
        #If it can't do this. Perhaps because values are not seperated by commas.
        #It doesn't crash the program.
        #Instead it prints an error message and reverts to the default csv file.
        except ValueError as Val:
            #Informs the user that an error has occurred.
            print("The program has encountered an error")
            print("File is not numbers, seperated by commas")
            #Tells the user what the error is.
            print ("Error message")
            print (ValueError)
            print(Val)
            #Tells the user what the program is doing about the error.
            print("Program reverting to inputting the default csv file")
            #Appends error messages to a file.
            error_message = ("Error. Perhaps text is in incorrect format")
            write_errors(error_message)
            error_message = str(ValueError) + ("\n")
            write_errors(error_message)
            error_message = str(Val) + ("\n")
            write_errors(error_message)            
            #Making sure a useable file is inputted.
            document = 'DEM.csv'
        except IOError as IO:
            print("File not found")
            print("Reverting to default file")
            print("Error message:")
            print(IOError)
            print(IO)
            #Appends error messages to a file.
            error_message = ("File not found")
            write_errors(error_message)
            error_message = str(IOError) + ("\n")
            write_errors(error_message)
            error_message = str(IO) + ("\n")
            write_errors(error_message)
            document = 'DEM.csv'
            dem = script.sesamie(document)
    #Same as above but for space seperated files.
    elif (document[-1]) == 't':
        try:
            dem = script.space(document)
        except ValueError as Val:
            print("The program has encountered an error")
            print("File is not composed of numbers sepearted by spaces")
            print ("Error message")
            print (ValueError)
            print(Val)
            #Appends error messages to a file.
            error_message = ("Something went wrong while reading the file into a list. Perhaps text is in incorrect format")
            write_errors(error_message)
            error_message = str(ValueError) + ("\n")
            write_errors(error_message)
            error_message = str(Val) + ("\n")
            write_errors(error_message)
            print("Program reverting to inputting the default text file")
            document = 'max.txt'
        except IOError as IO:
            print("File not found")
            print("Reverting to default file")
            print("Error message:")
            print(IOError)
            print(IO) 
            error_message = ("File not found")
            write_errors(error_message)
            error_message = str(IOError) + ("\n")
            write_errors(error_message)
            error_message = str(IO) + ("\n")
            write_errors(error_message)
            document = 'max.txt'
            dem = script.space(document)
    #Covers all other problems.
    else:
        #Lets the user know what the problem is.
        print("Error. Probably an invalid file extension.")
        print("Reverting to default DEM file")
        #Making sure a useable file is inputted.
        document = 'DEM.csv'
#Lets the user know if no name for the file has been entered.
#This could happen if the script_document function was not run.
else:
    print("No file found")

#User inputting how many times to run the model.
#Sets up a count so that the computer will assign a value to iteration if none entered.
#after a certain number of requests.
count = 0
#Number of times to run the model.
#Creates an infinate loop until broken by the continue command.
while True:
    #Try this.
    try:
        #Get user to input number of times to run the model.
        print("How many times would you like the model to run?")
        iteration = int(input("Enter a number between 1 and 10?:"))
        #If they suggest a number that is too high or low.
        if iteration < 1 or iteration > 10:
            #Increase the count of thier tries by one.
            count +=1
            print("That is not a valid entry")
            iteration = int(input("try again"))
            #If the have had less than 3 tries.
            if count < 3:
                #Loop back to the beginning (the while statement).
                continue
            #If a valid entry is still not fourthcoming after three prompts.
            else:
                #Inform the user that you are reverting to default value.
                print("You have not entered a valid number, reverting to default")
                print("This program will run one iteration of the model") 
                #Assign default value.
                iteration = 1
                #Stop looping through while statement.
                break
        #If a valid entry has been entered break out of the while loop.
        else:
            break 
    #If get an error trying the above, do this.         
    except ValueError as Val:
        #Increase the count of thier tries by one.
        count +=1
        #Inform user and write error messages to file.
        print("That value is not valid. The value must be a number.")
        print("Error message")
        error_message = ("Number not entered")
        write_errors(error_message)
        error_message = str(ValueError)
        write_errors(error_message)
        error_message = str(Val)
        write_errors(error_message)
        print(ValueError)
        print(Val)
        if count < 3:
            #Loop to beginning of while statement.
            continue
        #If had to many attempts.
        else:
            #Revert to default and explain this.
            print("You have not entered a valid number, reverting to default")
            print("This program will run one iteration of the model")
            iteration = 1
        break
    #If entry is correct, break out of while loop.
    else:
        break

#Attaching values to labels. 
#Location to move fairy dust to.    
location = script.map(dem)
#List with the accumulation of fairy dust in each cell.
store = script.store(location)
#Dustfall intensity.
amount = 3

#Checking that the dem and location list have been created properly.
print("Dem list")
print(dem)
print("Location list")
print(location)


#Creating the GUI.

#I've used information from the practical classes to help me create the GUI.
#But am using the grid instead of pack method to position elements in the frame.
#I have also changed the size of the window and canvas and added in labels.

#Settting up the GUI window.
root = tkinter.Tk()
#Gives the GUI a name which appears along the top bar of the window.
root.title("Dust Model")
#Sets the size of the GUI window.
root.geometry("800x400")
#Setting up a frame which can hold the other parts of the GUI together
#and can be used to position items
app = Frame(root)
#Used to place items in certain places in the GUI window.
app.grid()

#Text explaining what the model does. In the GUI window.
lbl = Label(app, text = "This model takes a DEM grid and produces an image of how fairy dust accumulates on the landscape after a dustfall event")
#Positions the text.
lbl.grid(row = 0, column = 0, columnspan = 3, sticky = W)
lbl2 = Label(app, text = "Choose from the menu options to run the model, see the model input grids")
lbl2.grid(row = 1, column = 0, columnspan = 3, sticky = W)

#Setting up the graph so that it can be animated.
fig = matplotlib.pyplot.figure()

#Function from the practical classes/assignment with the carry_on variable removed.
#Without this, the commands don't run.
#It waits for a command, the process it, then waits to be called again.
def gen_function (b = [0]):
    """Runs each time it is called.
    
    Positional arguements:
    b -- an interger number (default = 0)
    
    Returns:
    The value of a, which increases by one each time it is run.
    """
    #Setting up a count.
    a = 0
    #Running the model until it has been run the same number of times as the 
    #number of iterations requested.
    #This is done using the "a" counter.
    while (a < iteration): 
        #Gives the local value of a instead of reverting to the global variable
        #until the number of interations is greater or equal to a. 
        yield a			
        #Value of counter increases.
        a = a + 1


#Creating commands. These do something when menu item is clicked on.
#Used information from the practicals to help me with this function.
#As you can see, it is edited though.
#Creating a new store list each time fairy dust falls and moves across the landscape.
def update(frame_number):
    """
    Runs n iterations of the model.
    
    Positional arguements:
    frame_number -- integer value (no default)
    
    Returns:
    Final value in the store list after a certain number of iterations of the model have been run.
    """
    #Uses the global values of location and number of iterations without
    #having to pass these variables through the function.
    #Really useful to use global store as it means it can then be seen outside
    #of the function and therefore written to a file.
    global store
    global location
    global iteration
    #Starts off using the values of dust in each cell from the store function
    #which has produced a blank list of the correct size.
    store = script.store(location)
    #Clearing anything that is already displayed in the graph.
    fig.clear()
    #Creates a counter.
    a = 0
    #Loops through each iteration of the model.
    #Runs until a is the same as the number of iterations requested.
    while a < iteration:
        #Count, increases by one each time this part of the code is run.
        a +=1
        #Calls upon a function to generate fairy dust falling on the environment.
        rain = script.rain(location, amount)   
        #Uses the function to move the fairy dust between cells.
        store = script.move(location, store, rain)
        #Checking that this function is working correctly.
        print("Iteration")
        print(a)
        print("store")
        print(store)
        print("rain list")
        print(rain)
        #Plot the results of each iteration.
        #Setting up the length of the x and y axes.
        matplotlib.pyplot.ylim,(-0.5, len(store)-0.5)
        matplotlib.pyplot.xlim(-0.5, len(store)-0.5)
        #Plotting the graph.
        #Got information about how to add a colour scheme from https://matplotlib.org/api/cm_api.html
        matplotlib.pyplot.imshow(store, cmap = 'Blues')
        
#Creates image of the location grid.
def show(frame_number):
    """
    Create image of location grid.
    
    Positional arguements:
    frame_number -- integer value (no default)
    
    Returns:
    Image of location grid.
    """
    global location
    #Clear whatever image was previously been shown.
    fig.clear()
    #Set up axes.
    matplotlib.pyplot.ylim,(-0.5, len(location)-0.5)
    matplotlib.pyplot.xlim,(-0.5, len(location)-0.5)
    #Plot the image.
    image = matplotlib.pyplot.imshow(location)

#Creates image of the direction grid.
def direction(frame_number):
    """
    Create image of direction grid.
    
    Positional arguements:
    frame_number -- integer value (no default)
    
    Returns:
    Image of direction grid.
    """
    fig.clear()
    direct = [[6,7,8],[4,0,5],[1,2,3]]
    matplotlib.pyplot.ylim,(-0.5, 2.5)
    matplotlib.pyplot.xlim,(-0.5, 2.5)
    image = matplotlib.pyplot.imshow(direct)

#Creates an image of the dem grid.    
def topo(frame_number):
    """
    Create image of dem.
    
    Positional arguements:
    frame_number -- integer value (no default)
    
    Returns:
    Image of dem.
    """
    fig.clear()
    global dem
    matplotlib.pyplot.ylim,(-0.5, 6.5)
    matplotlib.pyplot.xlim,(-0.5, 6.5)
    image = matplotlib.pyplot.imshow(dem) 
 
    
#Images shown in the GUI canvas.
#Used the practical classes for these.
    
#Shows how the dust accumulation changes with each iteration of the model.
def run():
    """Run the animation."""
    #Explains to the user what the image shows.
    lbl.config(text = "Shows the accumulation of fairy dust on the landscape")
    lbl2.config(text = "")
    #Shows a graph of the values in the store list for each iteration of the model.
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False) 
    canvas.show()

#Shows location grid.  
def show_location():
    """Run the animation."""
    #Explains to the the user what the image shows.
    lbl.config(text = "Shows the direction of the steepest downhill slope from cell")
    lbl2.config(text = 'To see what colour the direction means select "show direction" from the show dropdown menu')
    animation = matplotlib.animation.FuncAnimation(fig, show, frames=gen_function, repeat=False)
    canvas.show()  

#Shows the direction grid.   
def direction_show():   
    """Run the animation."""
    #Explains to the the user what the image shows.
    lbl.config(text = "The colour on the cells is a key showing the direction")
    lbl2.config(text = "from the middle cell that fairydust would move.")
    animation = matplotlib.animation.FuncAnimation(fig, direction, frames=gen_function, repeat=False)
    canvas.show()       

#Shows the dem grid.    
def topo_show():
    """Run the animation."""
    #Explains the the user what the image shows.
    lbl.config(text = "Topographic map of the landscpae")
    lbl2.config(text = "")
    animation = matplotlib.animation.FuncAnimation(fig, topo, frames=gen_function, repeat=False)
    canvas.show() 

#Quits the program.
def quit_method():
    """Closes window when QUIT is clicked"""
    fig.clear()
    lbl.config(text = "Quit program")
    lbl2.config(text = "")
    #Creates a button, which when pressed closes the GUI window.
    QUIT = Button(app, text = "QUIT", command = root.destroy)
    #Positions the button on the window.
    QUIT.grid(row = 0, column = 0)

#Writes location to a file.  
def write_location():
    """Write contents to text file"""
    fig.clear()
    lbl.config(text = "Written location grid to file")
    lbl2.config(text = "File is called location_grid.txt")
    #Opens new file.
    f = open('location_grid.txt', 'w', newline='') 
    #Writes contents, putting a commas between values.
    writer = csv.writer(f, delimiter=',')
    #Loops through each row in the list.
    for row in location:		
       #Writes the rows to the textfile.
    	writer.writerow(row)
    #Closes the file.
    f.close() 

#Writes final store to a file.  
def write_store():
    """Write contents to text file"""
    fig.clear()
    lbl.config(text = "Written store grid to file")
    lbl2.config(text = "File is called dustlevel.txt")
    script.write(store)
  
    
#Menus
    
#Sets up menu items. Giving the user a choice parts of the software to use.
menu_bar = tkinter.Menu(app)
root.config(menu=menu_bar)

#Creating menus.
model_menu = tkinter.Menu(menu_bar)
image_menu = tkinter.Menu(menu_bar)
write_menu = tkinter.Menu(menu_bar)
quit_menu = tkinter.Menu(menu_bar)

#Naming the menu options.
menu_bar.add_cascade(label="run", menu=model_menu)
menu_bar.add_cascade(label="show", menu=image_menu)
menu_bar.add_cascade(label="write", menu=write_menu)
menu_bar.add_cascade(label="quit", menu=quit_menu)

#Creating the drowdown options and assigning commands to them.
model_menu.add_command(label="Run model", command=run) 
image_menu.add_command(label = "location", command=show_location)
image_menu.add_command(label = "direction", command=direction_show)
image_menu.add_command(label = "dem", command=topo_show)
write_menu.add_command(label = "location", command=write_location)
write_menu.add_command(label = "store", command=write_store)
quit_menu.add_command(label = "quit program", command=quit_method)


#Creating the canvas. This displays images.

#Sets up the size of the canvas.
c = tkinter.Canvas(app, width=50, height=50)
#Gives the location of the canvas.
c.grid(row = 3, column = 0)
#Plots images to the canvas.
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=app)
#Gives a position for the image in the canvas.
canvas._tkcanvas.grid(row = 4, column = 0)
#Displays the canvas in the GUI.
canvas.show()

#Opens the GUI window. Runs processes with prompted/data is inputted.
tkinter.mainloop()









