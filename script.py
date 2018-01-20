# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:21:54 2017

@author: kate
"""
#Importing scripts.
import os.path
import csv
import random

#numpy license
#Copyright © 2005-2017, NumPy Developers.
#All rights reserved.
import numpy

#Setting a seed so that the same random numbers are created on each run.
random.seed(a=5)


#Request name of file to be opened. Checks that entry is valid.
def document_input():
    """
    Requests file name and checks file is present.
    
    Returns:
    Returns name of file choice.
    """
    #Assigning variable values using user inputs.
    #Getting the user to input the name of the DEM file they want to use.
    #Setting up a count so that if the user fails to enter a correct file after a certain number
    #of tries the program will revert to the default.
    count = 0
    #Creating a blank document.
    doc_name = ""
    #Instructions on accepted file types.
    print("This model will only accept csv files that are comma delimted and txt files that are space delimited")
    #Details of what they can enter in case user is confused about inputs.
    print("Possible choices include DEM.csv and max.txt")
    #Continue prompting the user to enter a name of a file until they enter a file present in the folder.
    while doc_name == "":
        #Increase the count.
        count +=1
        #Get the user to enter the name of the file.
        doc_name = input("What is the name of your dem file?:")
        #Checking the file is present in the folder.
        #I got this code from http://net-informations.com/python/file/exists.htm
        #I have edited this code. The original code is:
        #import os.path
        #filename = "my_file.txt"
        #if(os.path.isfile(filename)):
        #   print("File Exists!!")
        #else:
        #    print("File does not exists!!")
        if(os.path.isfile(doc_name)):
            break
        else:
            doc_name = ""
            print("That folder is not present. Have you inluded the extension, e.g. csv or txt")
            print("Try entering DEM.csv or max.txt")
            if count > 3:
                print("Reverting to default")
                doc_name = 'DEM.csv'
            else:
                continue
    return doc_name

#Reads in text file seperated by commas.
#Uses information from the practical classes/assessment.
#But uses the with open method instead.
def sesamie(document):
    """
    Open a file representing coordinate values and convert it into a double list.
    
    Positional arguements:
    document -- file of comma seperated integer or float values (no default)
    
    Returns:
    Rows of the text file converted into a list, values within each row nested into the row list.
    """
    #Creates empty file for the dem coordinate values to be stored in later.
    dem = []
    #Opens the file in a manner that ensures it will close if the program crashes or a file is forgotten to be closed.
    #Opens up the file
    with open(document, 'r', newline='') as f:
        f = open(document, newline='')
        #Values converted from strings to floats.
        file = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)      
        #Converting the data from grid format to a double list format.
        #This is so the position of a value in a list can represent its x and y coordinate location.
        #Looping through the rows of data to create the first tier of the list, which represents the y coordinate position.
        for row in file:
            #Creating a list for all the values for each y coordinate line to go in.
            row_list = []
            #Looping through the values in the rows of data to give the x coordinate location.
            for value in row:
                #Adding the x coordinate values to the lists created for the y coordinates.
                row_list.append(value)
            #Adds the lists of the row data to a list of all the data arranged by rows.
            dem.append(row_list) 
    #Closing the file after use.
    f.close()
    return dem


#This is the code for def space() is taken from the website:
#https://stackoverflow.com/questions/12917588/reading-multiple-numbers-from-a-text-file
#with open("datafile") as f:
#    for line in f:  #Line is a string
#        #split the string on whitespace, return a list of numbers 
#        # (as strings)
#        numbers_str = line.split()
#        #convert numbers to floats
#        numbers_float = [float(x) for x in numbers_str]  #map(float,numbers_str) works too

#This is the code to read in a file where the numbers are seperated with spaces.
def space(document):
    """
    Open a file representing coordinate values and convert it into a double list.
    
    Positional arguements:
    document -- file of space seperated integer or float values (no default)
    
    Returns:
    Rows of the text file converted into a list, values within each row nested into the row list.
    """
    numbers = []
    with open(document, 'r') as f:
        for row in f:
            numbers_str = row.split()
            #convert numbers to floats
            numbers_int = [int(x) for x in numbers_str]
            numbers.append(numbers_int)
    f.close()
    return numbers


#Convert from a DEM of height values to a list of slope values.
#Then uses the slope values to determine the direction of greatest slope from the cell.
def map(dem):
    """
    Calculate the direction of greatest slope between a cell and its neighbours.
    
    Positional arguements:   
    dem -- double list of integer or float values (no default)
    
    Returns:
    Double list, z value is a code representing direction of greatest slope for each cell.
    """
    #Empty list for the code representing direction of adjeacent cell with greatest gradient to be stored in.
    location = []
    #Empty list for the value of the greatest gradient to be stored in.
    slope = []
    #Convert from a DEM of height values to a list of slope values.
    #Also produces a location list with a code as to which cell the water should move to.
    #Creating a list position for the y coordinate.
    #Uses the length of the dem so that code will operate on dems of varying size.
    for y in range(len(dem)):
        #Setting up lists to store the gradient and maximum gradient locations in.
        slope_row = []
        #The location list only shows the location in relation to the gradient list.
        #Therefore it's value is a code representing direction of steepest gradient.
        #So it needs decoding before use.
        location_row = []
        #Creating a list position for the y coordinate.
        for x in range(len(dem[y])):
            #Setting up a list to store the gradient values between the cell and its neighbours.
            gradient = []
            #Excluding cells at edge of DEM from analysis, as not known whether steepest gradient is off edge of map.
            if y>0 and x>0 and y<len(dem)-1 and x<len(dem[y])-1:
                #Formatting the code so that it still runs when cells are missing.
                try:         
                    #Finds the gradient between a cell and its neighbours.
                    gradient = [
                            (dem[x][y]-dem[x][y]),
                            (dem[y][x]-dem[y+1][x-1])/(2**0.5), 
                            (dem[y][x]-dem[y+1][x]), 
                            (dem[y][x]-dem[y+1][x+1])/(2**0.5), 
                            (dem[y][x]-dem[y][x-1]), 
                            (dem[y][x]-dem[y][x+1]), 
                            (dem[y][x]-dem[y-1][x-1])/(2**0.5), 
                            (dem[y][x]-dem[y-1][x]), 
                            (dem[y][x]-dem[y-1][x+1])/(2**0.5)
                            ]
                    #Adding the list of maximum gradients to all the values in the row.
                    slope_row.append(max(gradient))
                    #Adding the location of the first maximum gradient found for all the values in the row.
                    #Problem with this is that it only finds the first gradient in the list.
                    #Although maybe that's how fairy dust acts.
                    location_row.append(numpy.argmax(gradient))
                #Allowing the program to run, despite missing coordinates.
                except TypeError as TE:
                    #Telling the user that there is an error.
                    print (TypeError)
                    #Suggesting a reason for the error.
                    print("Something went wrong, perhaps there are not equal number of x coordinates for each line of y coordinates")                     
                    error_message = ("Error in map(dem) function, perhaps not equal numbers of coordinates in each row")
                    write_errors(error_message)
                    error_message = str(TypeError) + ("\n")
                    write_errors(error_message)
                    error_message = str(TE) + ("\n")
                    write_errors(error_message)
                #Catching anything else that might happen and continuing to run the program.
                else:
                    continue    
        #Creating grid of greastest slope for each cell.
        #This isn't needed for the program, but can be consulted to check the code.
        #Adding the gradient and location data for the rows to a list to give the x and y positions of this data.        
        slope.append(slope_row)
        #Creating a grid of direction of greatest slope from cell in question.
        location.append(location_row)
    #Removing the first and last entry in the list as these contain blank cells adjacent to them.
    #Therefore they are giving blank entries.
    location.remove(location[0])
    location.remove(location[len(location)-1])
    #Previous method of removing entries from the grid.
    #location = location[1:-1]
    #Returning the direction of greatest slope from cell in question.
    #This new grid is 2 cells smaller in both the x and y direction.
    #This is because this program does not want to calculate the direction of greatest slope when the value in certain directions is not known.
    return location


#Rainfall list
def rain(location, amount):
    """
    Create a double list of amount of rain falling on each cell.
    
    Positional arguement
    location -- double list of floats or integers (no default)
    
    Returns.
    Grid of amount of rain in each cell.
    """
    #Blank rainfall list.
    rain = []
    #Using the location grid to determine the size of the rainfall grid.
    #This means that function can be used for other sized grids.
    for i in range(len(location)):
        #Setting up blank list for data in the rows to be placed in.
        rain_row = []
        #Using the length of each row in the location list to determine the size of each rain row.
        for j in range(len(location[i])):
            #Mimicking the pattern of rain by randomly assigning the amount of rain in each cell within a narrow range.
            #Checking program is working by setting rain amount to be constant for each cell.
            #intensity = 2
            intensity = random.randint(amount,amount+3)
            #Adding the values to the row list
            rain_row.append(intensity)
        #Adding the values from each row to the grid
        rain.append(rain_row)
    #Returning a double list showing the amount of rain in each cell.
    return rain


#Blank grids for the amount of rain accumulating on the landscape to be stored in.
def store(location):
    """
    Create a blank list for the accumulation of water on the landscape to be stored in.
    
    Positional arguement
    location -- double list of floats or integers (no default)
    
    Returns:
    Blank lists of correct size required.
    """
    #Creating initial lists.
    store = []
    #A temporary store list is required for later fucntions.
    for i in range(len(location)):
        store_row = []
        #Creating blank values within the rows.
        for j in range(len(location[i])):
            value = 0
            #Adding the values to each row.
            store_row.append(value)
        #Adding the row values to the main list.
        store.append(store_row)
    #Outputting the blank store lists.
    return store


#Moving the water in the direction of steepest gradient.
def move(location, store, rain):
    """
    Move half of substance to adjacent cell with steepest gradient to that cell.
    
    Positional arguements:
    location -- double list of integer or float values (no default)
    store -- double list of integer or float values (no default)
    rain -- double list of integer or float values (no default)
    
    Returns:
    New store grid with accumulations of substance in each cell from neighbouring cells and from rainfall.
    """
    #Moving water
    #Creating loop
    temp_store = store
    for i in range(len(location)):
        
        for j in range(len(location[i])):
            store[i][j]=store[i][j]+rain[i][j]
#            temp_store[i][j]=store[i][j]
 #           temp_store[i][j]=temp_store[i][j]/2
            try:
                if location[i][j] == 0:
                    temp_store[i][j] = (store[i][j]/2+temp_store[i][j])
                elif location[i][j] == 1:
                    temp_store[i+1][j-1] = (store[i][j]/2+temp_store[i+1][j-1])
                elif location[i][j] == 2:
                    temp_store[i+1][j] = (store[i][j]/2+temp_store[i+1][j])
                elif location[i][j] == 3:
                    temp_store[i+1][j+1] = (store[i][j]/2)+(temp_store[i+1][j+1])
                elif location[i][j] == 4:
                    temp_store[i][j-1] = (store[i][j]/2)+(temp_store[i][j-1])
                elif location[i][j] == 5:
                    temp_store[i][j+1] = (store[i][j]/2)+(temp_store[i][j+1])  
                elif location[i][j] == 6:
                    temp_store[i-1][j-1] = (store[i][j]/2)+(temp_store[i-1][j-1])
                elif location[i][j] == 7:
                    temp_store[i-1][j] = (store[i][j]/2)+(temp_store[i-1][j])
                elif location[i][j] == 8:
                    temp_store[i-1][j+1] = (store[i][j]/2)+(temp_store[i-1][j+1])
            except IndexError:
                print(IndexError)
            else:
                continue
    #Putting the temp_store list back in store.
    store = temp_store
    #Returning subtance accumulations on landscape.
    return store
 
    
def write(store):
    """
    Write a double list to a text file.
    
    Positional arguements:
    store -- double list of integer or float values (no default)
    
    Returns:
    A text file, layed out as a grid, containing values extracted from a double list with values delimited by commas.
    """  
    #Open up the file to write to.
    f = open('dustlevel.txt', 'w', newline='') 
    writer = csv.writer(f, delimiter=',')
    #Loops through each row in the list.
    for row in store:		
       #Writes the rows to the textfile.
    	writer.writerow(row)
    #Closes the file.
    f.close()
    
def write_errors(error_message):  
    """Write error messages to a file
    
    Positional arguements:
    error_message -- string (no default)
    
    Returns:
    Error messages appended to a file.
    """
    text_file = open("Error_file.txt", "a")
    text_file.writelines(error_message)
    text_file.writelines("\n")
    text_file.close()
        