import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import serial
import threading
import time

class ArduinoControlApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Arduino Control")
        self.master.geometry("800x400")

        self.connect_button = tk.Button(self.master, text="Connect Arduino", command=self.connect_arduino)
        self.connect_button.pack(pady=10)

        self.send_button = tk.Button(self.master, text="Send 'hi' to Arduino", command=self.send_hi)
        self.send_button.pack(pady=10)

        # Create two ScrolledText widgets for sent and received data
        self.sent_terminal = ScrolledText(self.master, height=10, width=40, state=tk.DISABLED)
        self.sent_terminal.pack(side=tk.LEFT, padx=10)

        self.received_terminal = ScrolledText(self.master, height=10, width=40, state=tk.DISABLED)
        self.received_terminal.pack(side=tk.RIGHT, padx=10)

        self.ser = None

    def connect_arduino(self):
        try:
            # Adjust the serial port name and baud rate based on your Arduino configuration
            self.ser = serial.Serial('COM4', 230400)
            self.print_to_terminal("Arduino Connected Successfully!", terminal="received")
        except Exception as e:
            self.print_to_terminal(f"Failed to connect to Arduino: {e}", terminal="received", error=True)

    def send_hi(self):
        if self.ser:
            try:
                # Send "hi" to the Arduino
                self.ser.write(b'hi\n')
                self.print_to_terminal("Sent 'hi' to Arduino successfully!", terminal="sent")
            except Exception as e:
                self.print_to_terminal(f"Failed to send message to Arduino: {e}", terminal="sent", error=True)
        else:
            self.print_to_terminal("Please connect to Arduino first.", terminal="sent", error=True)

    def print_to_terminal(self, message, terminal="received", error=False):
        # Print messages to the specified terminal
        if terminal == "sent":
            text_widget = self.sent_terminal
        else:
            text_widget = self.received_terminal

        text_widget.config(state=tk.NORMAL)
        tag = "error" if error else "normal"
        text_widget.insert(tk.END, f"{message}\n", tag)
        text_widget.config(state=tk.DISABLED)
        text_widget.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ArduinoControlApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    
    # Create a separate thread for reading data from Arduino
    def read_serial():
        while True:
            if app.ser:
                try:
                    # Read a line from the serial port (blocking call)
                    data = app.ser.readline().decode('utf-8').strip()
                    
                    # Print received data to the received terminal
                    if data:
                        app.print_to_terminal(f"Received Data: {data}", terminal="received")
                except Exception as e:
                    app.print_to_terminal(f"Error reading data from Arduino: {e}", terminal="received", error=True)
                    break
            time.sleep(0.1)

    # Start the thread for reading data
    threading.Thread(target=read_serial, daemon=True).start()

    root.mainloop()

    # Close the serial port when the GUI is closed
    if app.ser:
        app.ser.close()
