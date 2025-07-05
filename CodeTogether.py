import random
import string
import tkinter as tk
from tkinter import filedialog, scrolledtext, Menu, simpledialog
import subprocess
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
import pyperclip

clients = []


class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")
        self.root.geometry("1366x768")  # Optimized for 15.6-inch screens
        self.root.configure(bg="#1E3A3A")  # Deep Teal-Blue Background
        self.timer_running = False
        self.timer_seconds = 0  # Track timer seconds
        self.current_file = None  # Track the current open file
        self.file_modified = True
        

        # Menu Bar (Dark Teal Theme)
        self.menu_bar = Menu(root, bg="#285252", fg="white", activebackground="#3C6E6E", activeforeground="white")
        root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0, bg="#285252", fg="white", activebackground="#3C6E6E")
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0, bg="#285252", fg="white", activebackground="#3C6E6E")
        self.edit_menu.add_command(label="Cut", command=lambda: self.coding_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=lambda: self.coding_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=lambda: self.coding_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Delete", command=self.delete_selected_text, accelerator="Del")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Run Menu
        self.run_menu = Menu(self.menu_bar, tearoff=0, bg="#285252", fg="white", activebackground="#3C6E6E")
        self.run_menu.add_command(label="Run", command=self.run_code, accelerator="F5")
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)

        # Custom Button Styles
        def style_button(btn, bg_color, hover_color):
            btn.config(font=("Arial", 11, "bold"), bg=bg_color, fg="white",
                       activebackground=hover_color, activeforeground="white", bd=0, relief=tk.FLAT, padx=10, pady=5)

        # Timer Buttons
        self.timer_button = tk.Button(root, text="▶", command=self.toggle_timer)  # Start/Pause Button
        style_button(self.timer_button, "#FF9800", "#E08900")
        self.timer_button.place(x=10, y=5, width=40, height=35)  # Positioned on the left

        self.reset_timer_button = tk.Button(root, text="🔄", command=self.reset_timer)  # Reset Timer Button
        style_button(self.reset_timer_button, "#FF5722", "#E04C1E")
        self.reset_timer_button.place(x=55, y=5, width=40, height=35)  # Positioned next to the timer button

        # Timer Label (Positioned Right of Timer Button)
        self.timer_label = tk.Label(root, text="00:00", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.timer_label.place(x=100, y=12)  # Positioned to the right of the timer buttons

        # Language Selection ComboBox 
        self.language_label = tk.Label(root, text="Language:", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.language_label.place(relx=0.53, y=12)

        self.language_combo = ttk.Combobox(root, values=["Python", "C", "Java"], font=("Arial", 12), state="readonly")
        self.language_combo.place(relx=0.60, y=12, width=100)
        self.language_combo.current(0)  # Default to Python
        self.language_combo.bind("<<ComboboxSelected>>", self.broadcast_language)


        # Room Info
        self.room_id = None
        self.room_creator = None

        # Create & Join Room Buttons
        self.create_room_button = tk.Button(root, text="Create Room", command=self.create_room_popup)
        self.join_room_button = tk.Button(root, text="Join Room", command=self.join_room_popup)

        # Create Room (Orange)
        style_button(self.create_room_button, "#FF5722", "#E04C1E")
        self.create_room_button.place(relx=0.72, y=5, width=140, height=35)

        # Join Room (Blue-Green)
        style_button(self.join_room_button, "#009688", "#00796B")
        self.join_room_button.place(relx=0.85, y=5, width=140, height=35)

        # Room ID & Creator Labels
        self.room_id_label = tk.Label(root, text="Room ID: None", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.room_id_label.place(relx=0.82, y=50)
        self.room_creator_label = tk.Label(root, text="Room Creator: None", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.room_creator_label.place(relx=0.82, y=75)

        # 📋 Copy Icon (No Visible Button)
        self.copy_icon = tk.Label(root, text="📋", font=("Arial", 12), fg="white", bg="#1E3A3A", cursor="hand2")
        self.copy_icon.place(relx=0.93, y=49)  # Slightly shifted right
        self.copy_icon.bind("<Button-1>", lambda e: self.copy_room_id())

        # User List Box (Styled)
        self.user_list_box = tk.Listbox(root, font=("Arial", 12), bg="#285252", fg="white", highlightthickness=2, highlightbackground="#FF9800", bd=0)
        self.user_list_box.place(relx=0.82, y=100, relwidth=0.16, relheight=0.75)
    
        # Coding Area 
        self.coding_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, font=("Courier", 14),
                                                     bg="#285252", fg="white", insertbackground="white")
        self.coding_area.place(x=10, y=50, relwidth=0.80, relheight=0.60)

        # Bind modification tracking
        self.coding_area.bind("<<Modified>>", self.on_text_change)
        self.coding_area.bind("<KeyRelease>", self.send_update)
        
        
        self.h_scroll_coding = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.coding_area.xview)
        self.coding_area.configure(xscrollcommand=self.h_scroll_coding.set)
        self.h_scroll_coding.place(x=10, rely=0.70, relwidth=0.80, height=15)

        # Input Frame
        self.input_label = tk.Label(root, text="Input:", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.input_label.place(x=10, rely=0.72)
        self.input_area = scrolledtext.ScrolledText(root, wrap="word", font=("Courier", 14),
                                                    bg="#3C6E6E", fg="white", insertbackground="white")
        self.input_area.place(x=10, rely=0.75, relwidth=0.24, relheight=0.23)
        self.input_area.bind("<Return>", self.run_input)  # Automatically sends input when Enter is pressed
        self.input_area.bind("<KeyRelease>", self.send_input)

        # Output Frame (Disabled Wrapping & Added Horizontal Scrollbar)
        self.output_label = tk.Label(root, text="Output:", font=("Arial", 12, "bold"), fg="white", bg="#1E3A3A")
        self.output_label.place(relx=0.26, rely=0.72)

        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.NONE, font=("Courier", 12),
                                                     bg="#263238", fg="lightgreen", insertbackground="white")
        self.output_area.place(relx=0.26, rely=0.75, relwidth=0.54, relheight=0.23)
        self.output_area.config(state=tk.DISABLED)

        self.h_scroll_output = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.output_area.xview)
        self.output_area.configure(xscrollcommand=self.h_scroll_output.set)
        self.h_scroll_output.place(relx=0.26, rely=0.98, relwidth=0.54, height=15)


        # Keyboard Shortcuts
        root.bind("<Control-n>", lambda event: self.new_file())
        root.bind("<Control-o>", lambda event: self.open_file())
        root.bind("<Control-s>", lambda event: self.save_file())
        root.bind("<Control-Shift-S>", lambda event: self.save_as())
        root.bind("<Control-q>", lambda event: root.quit())
        root.bind("<F5>", lambda event: self.run_code())

    def copy_room_id(self):
        """Copies the Room ID to clipboard."""
        if self.room_id:
            pyperclip.copy(self.room_id)
            self.copy_icon.config(text="✅")  # Change icon to ✅
            self.root.after(1000, lambda: self.copy_icon.config(text="📋"))  # Revert back after 1 second
            
    def create_room_popup(self):
        """Popup for creating a new room."""
        popup = tk.Toplevel(self.root)
        popup.title("Create Room")
        popup.geometry("300x200")
        popup.configure(bg="#1E3A3A")

        tk.Label(popup, text="Enter Your Name:", fg="white", bg="#1E3A3A").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)

        def submit():
            name = name_entry.get()
            if name:
                self.room_creator = name
                self.room_id = self.generate_room_id()
                self.room_id_label.config(text=f"Room ID: {self.room_id}")
                self.room_creator_label.config(text=f"Room Creator: {self.room_creator}")
                popup.destroy()
                self.start_server()

        tk.Button(popup, text="Create", command=submit, bg="#FF5722", fg="white").pack(pady=10)

    def join_room_popup(self):
        """Popup for joining an existing room."""
        popup = tk.Toplevel(self.root)
        popup.title("Join Room")
        popup.geometry("300x200")
        popup.configure(bg="#1E3A3A")

        tk.Label(popup, text="Enter Your Name:", fg="white", bg="#1E3A3A").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)

        tk.Label(popup, text="Enter Room ID:", fg="white", bg="#1E3A3A").pack(pady=5)
        room_entry = tk.Entry(popup)
        room_entry.pack(pady=5)

        def submit():
            name = name_entry.get()
            room_id = room_entry.get()
            if name and room_id:
                self.room_creator = name
                self.room_id = room_id
                try:
                    # Connect to the server and send the room ID
                    global client_socket
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(("127.0.0.1", 12345))
                    client_socket.send(room_id.encode())

                    # Wait for the server's response
                    response = client_socket.recv(1024).decode()
                    if response == "VALID_ROOM":
                        self.room_id_label.config(text=f"Room ID: {self.room_id}")
                        self.room_creator_label.config(text=f"Room Creator: {self.room_creator}")
                        threading.Thread(target=self.receive_updates, daemon=True).start()
                        popup.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid Room ID. Please try again.")
                        client_socket.close()
                except ConnectionRefusedError:
                    messagebox.showinfo("Info", "No server available. Please create a room first.")


        tk.Button(popup, text="Join", command=submit, bg="#009688", fg="white").pack(pady=10)

    def generate_room_id(self):
        """Generates a unique room ID."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def toggle_timer(self):
        """Toggles the timer between start and pause."""
        if self.timer_running:
            self.timer_running = False
            self.timer_button.config(text="▶", bg="#FF9800")  # Change to Play Icon
        else:
            self.timer_running = True
            self.timer_button.config(text="⏸", bg="#E04C1E")  # Change to Pause Icon
            self.update_timer()

    def reset_timer(self):
        """Resets the timer to 00:00 and stops it."""
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")
        self.timer_button.config(text="▶", bg="#FF9800")  # Change back to Play Icon

    def update_timer(self):
        """Updates the timer every second."""
        if self.timer_running:
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")  # Update the timer display
            self.root.after(1000, self.update_timer)  # Update every 1 second
    
    def new_file(self):
        self.current_file = None
        self.coding_area.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("Java Files", "*.java"), ("C Files", "*.c")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.coding_area.delete("1.0", tk.END)
                self.coding_area.insert(tk.END, file.read())
            self.current_file = file_path
            

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.coding_area.get("1.0", tk.END))
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                 filetypes=[("Python Files", "*.py"), ("Java Files", "*.java"), ("C Files", "*.c")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.coding_area.get("1.0", tk.END))
            self.current_file = file_path
            

    def delete_selected_text(self):
        self.coding_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def on_text_change(self, event=None):
        """Marks the file as modified when text is changed."""
        self.file_modified = True
        self.coding_area.edit_modified(False)  # Reset modification flag
    
    def read_output(self):
        """Reads and displays output from the running process."""
        while self.process and self.process.poll() is None:
            output = self.process.stdout.readline()
            if output:
                self.output_area.config(state=tk.NORMAL)
                self.output_area.insert(tk.END, output)
                self.output_area.see(tk.END)
                self.output_area.config(state=tk.DISABLED)

        # Capture remaining output
        output, error = self.process.communicate()
        if output:
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, output)
            self.output_area.config(state=tk.DISABLED)
        if error:
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, error)
            self.output_area.config(state=tk.DISABLED)

    def run_input(self, event=None):
        """Sends user input from the input area to the running Python script automatically."""
        if self.process and self.process.poll() is None:
            user_input = self.input_area.get("1.0", tk.END).strip()  # Read input from the text box
            if user_input:
                self.process.stdin.write(user_input + "\n")  # Send input to the process
                self.process.stdin.flush()  # Ensure input is sent immediately
                self.input_area.delete("1.0", tk.END)  # Clear input area after sending
    
    def run_code(self):
        if not self.current_file or self.file_modified:
            # Ask user to save the file before running
            save_before_run = messagebox.askyesno("Save File", "You have unsaved changes. Do you want to save before running?")
            if save_before_run:
                self.save_file()
            else:
                return  # Stop execution if user cancels saving

        # Get the selected language
        selected_language = self.language_combo.get()

        # Determine the command to run based on the selected language
        if selected_language == "Python":
            command = f'python "{self.current_file}"'
        elif selected_language == "C":
            # Compile and run C code
            executable = self.current_file.replace(".c", ".exe")
            compile_command = f'gcc "{self.current_file}" -o "{executable}"'
            compile_process = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
            if compile_process.returncode != 0:
                # Display compilation errors
                output = compile_process.stderr
            
            # Run the compiled executable
            command = f'"{executable}"'
        elif selected_language == "Java":
            # Compile and run Java code
            class_name = self.current_file.split("/")[-1].replace(".java", "")
            compile_command = f'javac "{self.current_file}"'
            run_command = f'java -cp "{"/".join(self.current_file.split("/")[:-1])}" {class_name}'
            compile_process = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
            if compile_process.returncode != 0:
                output = compile_process.stderr

            command = run_command
        else:
            messagebox.showerror("Error", f"Unsupported language: {selected_language}")
            return
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = process.stdout if process.stdout else process.stderr

        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, output)
        self.output_area.config(state=tk.DISABLED)

        self.broadcast_output(output)

    def start_server(self):
        global server, clients, valid_room_id
        valid_room_id = self.room_id  # Store the room ID
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 12345))
        server.listen()
        threading.Thread(target=self.accept_clients, daemon=True).start()
        messagebox.showinfo("Info", "Waiting for others to join....")

    def accept_clients(self):
        while True:
            client, addr = server.accept()
            clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        try:
            # Receive the room ID from the client
            room_id = client.recv(1024).decode()
            if room_id != valid_room_id:
                # If the room ID is invalid, reject the client
                client.send("INVALID_ROOM".encode())
                client.close()
                return
            else:
                # If the room ID is valid, notify the client
                client.send("VALID_ROOM".encode())

            # Add the client to the list of connected clients
            clients.append(client)
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break

                if data.startswith("CODE:"): 
                    self.update_coding_area(data[5:])
                    self.broadcast(f"CODE:{data[5:]}", client)
                elif data.startswith("INPUT:"):
                    self.update_input_area(data[6:])
                    self.broadcast(f"INPUT:{data[6:]}", client)
                elif data.startswith("OUTPUT:"):
                    self.update_output_area(data[7:])
                    self.broadcast(f"OUTPUT:{data[7:]}", client)
                elif data.startswith("LANGUAGE:"):
                    self.update_language_combo(data[9:])
                    self.broadcast(f"LANGUAGE:{data[9:]}", client)
        except:
            if client in clients:
                clients.remove(client)
            

    def broadcast(self, data, sender=None):
        for client in clients:
            if client != sender:
                try:
                    client.send(data.encode())
                except:
                    clients.remove(client)

    def connect_to_server(self):
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(("127.0.0.1", 12345))
            threading.Thread(target=self.receive_updates, daemon=True).start()
        except ConnectionRefusedError:
            messagebox.showinfo("Info", "No server available. Please create a room first.")

    def receive_updates(self):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if data.startswith("CODE:"):
                    self.update_coding_area(data[5:])
                elif data.startswith("INPUT:"):
                    self.update_input_area(data[6:])
                elif data.startswith("OUTPUT:"):
                    self.update_output_area(data[7:])
                elif data.startswith("LANGUAGE:"):
                    self.update_language_combo(data[9:])
            except:
                break

    def update_coding_area(self, data):
        self.coding_area.delete(1.0, tk.END)
        self.coding_area.insert(tk.END, data)

    def update_input_area(self, data):
        self.input_area.delete(1.0, tk.END)
        self.input_area.insert(tk.END, data)

    def update_output_area(self, data):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, data)
        self.output_area.config(state=tk.DISABLED)
    
    def update_language_combo(self, language):
        """Updates the language combo box with the received language."""
        self.language_combo.set(language)

    def send_update(self, event):
        if 'client_socket' in globals():
            data = self.coding_area.get(1.0, tk.END)
            client_socket.send(f"CODE:{data}".encode())
        elif 'server' in globals():
            data = self.coding_area.get(1.0, tk.END)
            self.broadcast(f"CODE:{data}")

    def broadcast_output(self, output):
        if 'client_socket' in globals():
            client_socket.send(f"OUTPUT:{output}".encode())
        elif 'server' in globals():
            self.broadcast(f"OUTPUT:{output}")

    def send_input(self, event=None):
        user_input = self.input_area.get("1.0", tk.END).strip()
        if user_input:
            if 'client_socket' in globals():
                client_socket.send(f"INPUT:{user_input}".encode())
            elif 'server' in globals():
                self.broadcast(f"INPUT:{user_input}")
            #self.update_input_area(user_input)
    
    def broadcast_language(self, event=None):
        """Broadcasts the selected language to all connected clients."""
        selected_language = self.language_combo.get()
        if 'client_socket' in globals():  # If connected as a client
            client_socket.send(f"LANGUAGE:{selected_language}".encode())
        elif 'server' in globals():  # If it's the server, broadcast changes
            self.broadcast(f"LANGUAGE:{selected_language}")


if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()
