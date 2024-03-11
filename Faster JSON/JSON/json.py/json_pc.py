import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial
import json

# Global variable for json_data
json_data = ""

# Function to send data to ESP8266
def send_data():
    global json_data  # Declare json_data as a global variable
    x_value = x_entry.get()
    y_value = y_entry.get()
    cmd_value = cmd_entry.get()

    data = {"x": int(x_value), "y": int(y_value), "cmd": cmd_value}
    json_data = json.dumps(data)

    # Sending data to ESP8266
    ser.write(json_data.encode())

    # Display sent data
    sent_data_text.insert(tk.END, f"Sent: {json_data}\n")

# Function to update the GUI with received data
def receive_data():
    # Reading data from ESP8266
    received_data = ser.readline().decode('utf-8', errors='replace')

    if received_data:
        try:
            # Parsing and displaying received data
            data = json.loads(received_data.strip())
            received_label.config(text=f"Received: {data}")

            # Display received data side by side
            received_data_text.insert(tk.END, f"Received: {data}\n")

            # Display sent data side by side
            sent_data_text.insert(tk.END, f"Sent: {json_data}\n")

        except json.JSONDecodeError:
            received_label.config(text="Error decoding JSON")

        # Scroll to the end of the received data
        received_data_text.yview(tk.END)
        sent_data_text.yview(tk.END)

    # Schedule the next check for received data
    root.after(10, receive_data)

# Set up serial communication with ESP8266 on COM6
ser = serial.Serial("COM6", 921600, timeout=0.1)  # Decreased timeout for faster response

# Create the main window
root = tk.Tk()
root.title("ESP8266 Communication")

# Create and place GUI elements
x_label = ttk.Label(root, text="X:")
x_label.grid(row=0, column=0, padx=5, pady=5)

x_entry = ttk.Entry(root)
x_entry.grid(row=0, column=1, padx=5, pady=5)

y_label = ttk.Label(root, text="Y:")
y_label.grid(row=1, column=0, padx=5, pady=5)

y_entry = ttk.Entry(root)
y_entry.grid(row=1, column=1, padx=5, pady=5)

cmd_label = ttk.Label(root, text="Command:")
cmd_label.grid(row=2, column=0, padx=5, pady=5)

cmd_entry = ttk.Entry(root)
cmd_entry.grid(row=2, column=1, padx=5, pady=5)

send_button = ttk.Button(root, text="Send Data", command=send_data)
send_button.grid(row=3, column=0, columnspan=2, pady=10)

received_label = ttk.Label(root, text="Received: ")
received_label.grid(row=4, column=0, columnspan=2, pady=5)

# Create scrolled text widgets to display sent and received data
received_data_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
received_data_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

sent_data_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
sent_data_text.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

# Periodically check for received data
root.after(10, receive_data)  # Decreased interval for faster updates

# Run the GUI
root.mainloop()
