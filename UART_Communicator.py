# UART_Communicator Application
# A user interface designed to communicate with the UART serial port and allow manipulation of the state machine designed in keil
# Author: Kareem El-Hajjar (101109259)
# Last modified: NOV/27/2020 

# Libraries
import serial
from tkinter import *
from time import sleep
import threading
import continuous_threading

# Initialize current_state variable used to track current state
current_state = 0

# Tkinter window initilization
root = Tk()
root.title("UART Communicator")
root.configure(background = 'black')
root.geometry("340x130")

# Constants
STATE1 = 1
STATE2 = 2
STATE3 = 3
STATE4 = 4

# Serial port Configuration
board = serial.Serial(port='COM5', baudrate=9600, timeout=1)
sleep(1)

def check_state():
    ''' Used to read the UART port and determine the current message to display 
        on the UI(also prints current_state in console for debugging) '''

    read_byte = int.from_bytes(board.read(),byteorder = "little")   # Reads one byte from the port and converts to integer

    global current_state    # Retrieves current_state as a global variable

    print(current_state)    # Displays current_state in console

    # Based on the appropiate recieved byte output appropriate message on the UI and change the state
    if(read_byte == 49):
        current_state = STATE1
        state_label = Label(root, text = "   LED1 OFF | LED2 OFF  ",font=("Monokai", 20)).place(x=5, y=80)
    elif(read_byte == 50):
        current_state = STATE2
        state_label = Label(root, text = "   LED1 OFF | LED2 ON  ",font=("Monokai", 20)).place(x=5, y=80)
    elif(read_byte == 51):
        current_state = STATE3
        state_label = Label(root, text = "   LED1 ON  | LED2 OFF  ",font=("Monokai", 20)).place(x=5, y=80)
    elif(read_byte == 52):
        current_state = STATE4
        state_label = Label(root, text = "   LED1 ON  | LED2 ON  ",font=("Monokai", 20)).place(x=5, y=80)
    

def change_state(user_input):
    ''' change_state function used to send next and previous intructions to the port '''
    if(user_input == 1):
        board.write(bytes('N', 'utf-8'))
    elif(user_input == 2):
        board.write(bytes('P', 'utf-8'))

# Configure next and previous buttons on UI
next_button = Button(root, text = "NEXT",command = lambda: change_state(1),font=("Monokai", 26),bg = "green").place(x=215, y=5)
previous_button = Button(root, text = "PREVIOUS",command = lambda: change_state(2),font=("Monokai", 26),bg = "red").place(x=5, y = 5)

# Configure and run a periodic thread updating the current state every millisecond
tl = continuous_threading.PeriodicThread(0.1,check_state)
tl.start()

# Run mainloop for UI
root.mainloop()
