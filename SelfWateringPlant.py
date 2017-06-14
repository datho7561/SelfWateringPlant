# Final Project for TEJ 4M
# Purpose: to water one or more plants automatically,
#   based on the reading on a soil moisture sensor,
#   and to report data on the plant back to the user
# Created By: David Thompson
#

# Import the windowing library
from tkinter import *

# Initialize some variables
global numPlants
numPlants = 0

# Execute when submit button is pressed
def submitListener():
    try:
        numPlants = int(inputEntry.get())
        print("Sucessfully changed num of plants")
    except ValueError:
        print("Failed to change num of plants")
        pass
    inputEntry.delete(0, END)

# Create the window
window = Tk()

# CREATE THE GUI ELEMENTS #

# Text explaining input field
prompt = StringVar()
prompt.set("Number of Plants")
inputText = Label(window, textvariable=prompt)

# Input field
inputEntry = Entry(window)

# Button
submitButton = Button(window, text="Set", command=submitListener)

# Elements for outputting data

# Variables for holding
temp = StringVar()
light = StringVar()
humidity = StringVar()

# Elements for title
tempLabel = Label(window, text="Temperature:")
lightLabel = Label(window, text="Light:")
humidityLabel = Label(window, text="Humidity:")

# 
tempValLabel =
lightValLabel =
humidityValLabel =

# Put elements onto window
inputText.grid(row=0, column=0)
inputEntry.grid(row=1, column=0)
submitButton.grid(row=2, column=0)


