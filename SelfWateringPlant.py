#######################################################
# Final Project for TEJ 4M
# Purpose: To water one or more plants automatically,
#   based on the reading on a soil moisture sensor,
#   and to report data on the plant back to the user,
#   in the form of a GUI.
# Created By: datho7561
# Works in: Python 2.7.9
#######################################################


# IMPORTING #

# Import the windowing library
from Tkinter import *
# Import the GPIO library
import RPi.GPIO as GPIO
# Import the Adafruit SPI and MCP3008 libraries to talk to the ADC chip
#import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# GUI CLASS #
# All of the work is done within this class
class PlantWindow(Tk):

    # CONSTANTS #

    # Colours for the GUI
    GREY = "#444"
    GREEN = "#0F8"

    # Time constants for sensor refresh and watering time per plant
    # (in millis)
    PLANT_TIME = 2000
    SENSOR_TIME = 30000

    # METHODS #

    # Creates the window
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        return

    # For resetting all the string variables
    def setStrings(self):
        self.plantsStr.set(self.numPlants)
        self.tempStr.set(str(int(self.temp)) + " C")
        self.lightStr.set(str(int(self.light)) + " %")
        self.moistureStr.set(str(int(self.moisture)) + " %")
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

    # Close the solenoid
    def closeSolenoid(self):
        GPIO.output(self.SOLENOID, GPIO.LOW)
        return

    # Takes a reading from the sensors, update the GUI, and if necessary waters the plants
    def checkSensors(self):

        print("Reading Sensors")

        # Send power to the moisture sensor
        GPIO.output(self.MOISTURE, GPIO.HIGH)
        
        # Read the sensor values
        self.moisture = self.mcp.read_adc(0)
        self.light = self.mcp.read_adc(1)
        self.temp = self.mcp.read_adc(2)

        # TODO: remove debug
        print(self.moisture)
        print(self.light)
        print(self.temp)

        # Convert the sensor values
        self.temp = ((3.3*self.temp/1024.0)-.6)*100
        self.light /= 10.24 # To a percentage (i.e. 100 is full)
        self.moisture /= 10.24 # To a percentage (i.e. 100 is full)

        # If the soil moisture id below 50% and there are plants
        if (self.moisture < 50 and self.numPlants > 0):
            # Open the valve
            GPIO.output(self.SOLENOID, GPIO.HIGH)
            # If the plants take less time to water than the refresh rate
            if (self.PLANT_TIME * self.numPlants < self.SENSOR_TIME):
                # Water the plants for a time proportional to the number
                # of plants
                self.after(self.PLANT_TIME*self.numPlants, self.closeSolenoid)
            else:
                # Water the plants until the next sensor reading
                self.after(self.SENSOR_TIME, self.closeSolenoid)

        # Disable power to the moisture sensor (this slows down oxidization)
        GPIO.output(self.MOISTURE, GPIO.LOW)
        
        # Refresh the readings on the GUI
        self.setStrings()

        # After a set amount of time, rerun this method
        self.after(self.SENSOR_TIME, self.checkSensors)
        return

    # Set up the GPIOs for interacting with the hardware
    def hardwareSetup(self):

        # Pin numbers for the MCP3004
        # NOTE: Using BCM numbers
        self.CLK = 18
        self.MISO = 23
        self.MOSI = 24
        self.CS = 25

        # Setup comminucation with the ADC using the Adafruit code
        self.mcp = Adafruit_MCP3008.MCP3008(clk=self.CLK,
                                            cs=self.CS, miso=self.MISO,
                                            mosi=self.MOSI)

        # Pins for other components
        # NOTE: Using BCM numbers
        self.SOLENOID = 4
        self.MOISTURE = 17

        # Setup the GPIOs
        GPIO.setup(self.SOLENOID, GPIO.OUT)
        GPIO.setup(self.MOISTURE, GPIO.OUT)
        return

    # Sets up the program
    def initialize(self):

        # Initialize Hardware
        self.hardwareSetup()
        
        # Window stuff
        self.grid() # layout manager
        self.resizable(False, False) # stop the window from being resized
        self.title("Self Watering Plant") # set the window title
        self.config(bg=self.GREY, highlightthickness=0)

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
        self.plantLabel = Label(self, text="Number of Plants:", anchor=NW,
                                width=15, bg=self.GREY, fg=self.GREEN)
        self.tempLabel = Label(self, text="Temperature:", anchor=NW,
                               width=15, bg=self.GREY, fg=self.GREEN)
        self.lightLabel = Label(self, text="Light:", anchor=NW,
                                width=15, bg=self.GREY, fg=self.GREEN)
        self.moistureLabel = Label(self, text="Moisture:", anchor=NW,
                                   width=15, bg=self.GREY, fg=self.GREEN)

        # The different values
        self.plantValLabel = Label(self, textvariable=self.plantsStr, anchor=NW,
                                   width=8, bg=self.GREY, fg=self.GREEN)
        self.tempValLabel = Label(self, textvariable=self.tempStr, anchor=NW,
                                  width=8, bg=self.GREY, fg=self.GREEN)
        self.lightValLabel = Label(self, textvariable=self.lightStr, anchor=NW,
                                   width=8, bg=self.GREY, fg=self.GREEN)
        self.moistureValLabel = Label(self, textvariable=self.moistureStr,
                                      anchor=NW, width=8,
                                      bg=self.GREY, fg=self.GREEN)

        # Text explaining input field
        self.inputText = Label(self, text="Set # Plants", width=15,
                               bg=self.GREY, fg=self.GREEN)

        # Input field
        self.inputEntry = Entry(self, width=10, bg=self.GREY, fg=self.GREEN,
                                highlightbackground=self.GREEN)

        # Button
        self.submitButton = Button(self, text="Set", command=self.submitListener,
                                   width=7, bg=self.GREY, fg=self.GREEN,
                                   highlightbackground=self.GREEN)

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

        # Start the timed event that reads the sensors periodically
        self.checkSensors()

        return


# Create the window
window = PlantWindow(None)

# Run the window
window.mainloop()

# Cleanup the GPIO when the program is closed
GPIO.cleanup()
