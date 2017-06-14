# Final Project for TEJ 4M
# Purpose: to water one or more plants automatically,
#   based on the reading on a soil moisture sensor,
#   and to report data on the plant back to the user
# Created By: datho7561
#

# Import the windowing library
from tkinter import *
# Import the GPIO library
import RPi.GPIO as GPIO

# Declare and initialize some global variables
global numPlants
global temp
global light
global moisture
numPlants = 0
temp = 20
light = 0.5
moisture = 420

# Create the window
window = Tk()

# Do this next. Why? Because Python.
# Variables for holding strings of sensor readings
plantsStr = StringVar()
tempStr = StringVar()
lightStr = StringVar()
moistureStr = StringVar()

# For resetting all the string variables
def setStrings():
    plantsStr.set(numPlants)
    tempStr.set(temp)
    lightStr.set(light)
    moistureStr.set(moisture)
    window.update()

setStrings()

# CREATE THE GUI ELEMENTS #

# Labels for the different values
plantLabel = Label(window, text="Number of Plants:")
tempLabel = Label(window, text="Temperature:")
lightLabel = Label(window, text="Light:")
moistureLabel = Label(window, text="Moisture:")

# The different values
plantValLabel = Label(window, textvariable=plantsStr, bg="#FFF")
tempValLabel = Label(window, textvariable=tempStr, bg="#FFF")
lightValLabel = Label(window, textvariable=lightStr, bg="#FFF")
moistureValLabel = Label(window, textvariable=moistureStr, bg="#FFF")

# Text explaining input field
prompt = StringVar()
prompt.set("Set # Plants:")
inputText = Label(window, textvariable=prompt)

# Input field
inputEntry = Entry(window)

# Execute when submit button is pressed
def submitListener():
    try:
        numPlants = int(inputEntry.get())
        print("Sucessfully changed num of plants")
    except ValueError:
        print("Failed to change num of plants")
        pass
    inputEntry.delete(0, END)
    setStrings()

# Button
submitButton = Button(window, text="Set", command=submitListener)

# PUT ELEMENTS ONTO GUI #
inputText.grid(row=0, column=0)
inputEntry.grid(row=1, column=0)
submitButton.grid(row=2, column=0)

plantLabel.grid(row=0, column=1)
tempLabel.grid(row=1, column=1)
lightLabel.grid(row=2, column=1)
moistureLabel.grid(row=3, column=1)

plantValLabel.grid(row=0, column=2)
tempValLabel.grid(row=1, column=2)
lightValLabel.grid(row=2, column=2)
moistureValLabel.grid(row=3, column=2)


