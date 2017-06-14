#######################################################
# Final Project for TEJ 4M
# Purpose: To water one or more plants automatically,
#   based on the reading on a soil moisture sensor,
#   and to report data on the plant back to the user,
#   in the form of a GUI.
# Created By: datho7561
#######################################################


# IMPORTING #

# Import the windowing library
from tkinter import *
# Import the GPIO library
import RPi.GPIO as GPIO


# GUI CLASS #
# All of the work is done within this class
class PlantWindow(Tk):

    # Colours for the GUI
    grey = "#444"
    green = "#0F8"

    # Creates the window
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        return

    # For resetting all the string variables
    def setStrings(self):
        self.plantsStr.set(self.numPlants)
        self.tempStr.set(self.temp)
        self.lightStr.set(self.light)
        self.moistureStr.set(self.moisture)
        self.update()
        return

    # Execute when submit button is pressed
    def submitListener(self):
        try:
            self.numPlants = int(self.inputEntry.get())
        except ValueError:
            pass
        self.inputEntry.delete(0, END)
        self.setStrings()
        return

    # Takes a reading from the sensors, update the GUI, and if necessary waters the plants
    def checkSensors(self):

        print("Finish me! I need to read the sensors and water the plant")

        # Need to do this to refresh the readings on the GUI
        self.setStrings()

        # Should be last statement in the method
        # after 30 seconds, rerun this code
        self.after(30000, self.checkSensors)

    # Sets up the window
    def initialize(self):

        # Window stuff
        self.grid() # layout manager
        self.resizable(False, False) # stop the window from being resized
        self.title("Self Watering Plant") # set the window title
        self.config(bg=self.grey, highlightthickness=0)

        # Variables for sensor values
        self.numPlants = 0
        self.temp = 20
        self.light = 0.5
        self.moisture = 0.5
        
        # Variables for holding strings of sensor readings
        self.plantsStr = StringVar()
        self.tempStr = StringVar()
        self.lightStr = StringVar()
        self.moistureStr = StringVar()

        # CREATE THE GUI ELEMENTS #

        # Labels for the different values
        self.plantLabel = Label(self, text="Number of Plants:", anchor=NW, width=15,
                                bg=self.grey, fg=self.green)
        self.tempLabel = Label(self, text="Temperature:", anchor=NW, width=15,
                               bg=self.grey, fg=self.green)
        self.lightLabel = Label(self, text="Light:", anchor=NW, width=15,
                                bg=self.grey, fg=self.green)
        self.moistureLabel = Label(self, text="Moisture:", anchor=NW, width=15,
                                   bg=self.grey, fg=self.green)

        # The different values
        self.plantValLabel = Label(self, textvariable=self.plantsStr, anchor=NW, width=8,
                                   bg=self.grey, fg=self.green)
        self.tempValLabel = Label(self, textvariable=self.tempStr, anchor=NW, width=8,
                                  bg=self.grey, fg=self.green)
        self.lightValLabel = Label(self, textvariable=self.lightStr, anchor=NW, width=8,
                                   bg=self.grey, fg=self.green)
        self.moistureValLabel = Label(self, textvariable=self.moistureStr, anchor=NW, width=8,
                                      bg=self.grey, fg=self.green)

        # Text explaining input field
        self.inputText = Label(self, text="Set # Plants", width=15,
                               bg=self.grey, fg=self.green)

        # Input field
        self.inputEntry = Entry(self, width=10,
                                bg=self.grey, fg=self.green, highlightbackground=self.green)

        # Button
        self.submitButton = Button(self, text="Set", command=self.submitListener, width=7,
                                   bg=self.grey, fg=self.green, highlightbackground=self.green)

        # PUT ELEMENTS ONTO GUI #
        self.inputText.grid(row=0, column=0)
        self.inputEntry.grid(row=1, column=0)
        self.submitButton.grid(row=2, column=0)

        self.plantLabel.grid(row=0, column=1)
        self.tempLabel.grid(row=1, column=1)
        self.lightLabel.grid(row=2, column=1)
        self.moistureLabel.grid(row=3, column=1)

        self.plantValLabel.grid(row=0, column=2)
        self.tempValLabel.grid(row=1, column=2)
        self.lightValLabel.grid(row=2, column=2)
        self.moistureValLabel.grid(row=3, column=2)

        # Set the strings to their default values
        self.setStrings()

        # Start the timed event that reads the sensors
        # After 30 000 millis, perform
        self.after(30000, self.checkSensors)

        return


# Create the window
window = PlantWindow(None)
window.mainloop()

