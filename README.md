# CodeTogether - Collaborative Python, C, and Java IDE

CodeTogether is a collaborative desktop IDE built with Python and Tkinter, supporting real-time code sharing, multi-language editing (Python, C, Java), and synchronized input/output between users in a shared room. It is designed for pair programming, teaching, and remote code interviews.

## Features

- **Multi-language Support:** Edit and run Python, C, and Java code.
- **Collaborative Editing:** Real-time code, input, and output synchronization across users in the same room.
- **Room System:** Create or join rooms using unique Room IDs.
- **User List:** See who is in your room (UI placeholder).
- **Clipboard Integration:** Copy Room ID with a single click.
- **Timer:** Built-in timer for coding sessions.
- **File Operations:** New, Open, Save, and Save As for code files.
- **Keyboard Shortcuts:** Common shortcuts for file and run actions.
- **Customizable UI:** Modern, dark-themed interface optimized for 15.6-inch screens.

## Installation

### Prerequisites

- **Python 3.7+** (https://www.python.org/downloads/)
- **pip** (Python package manager)
- **GCC** (for C code compilation)
- **Java JDK** (for Java code compilation and execution)

### Required Python Packages

Install the required packages using pip:

```sh
pip install pyperclip
pip install tkinter
pip install socket
pip install threading
```

Tkinter is included with most Python installations. If not, install it via your OS package manager.

### For C and Java Support

- **GCC:** Install via [MinGW](http://www.mingw.org/) (Windows) or your OS package manager.
- **Java JDK:** Download and install from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.java.net/install/).

Ensure `gcc`, `g++`, `gdb`, and `javac` are in your system PATH.

## Usage

1. **Clone or Download the Repository**

   ```sh
   git clone [https://github.com/yourusername/CodeTogether.git
   cd CodeTogether
   ```

2. **Run the Application**

   ```sh
   python CodeTogether.py
   ```

3. **Create or Join a Room**
   - Click "Create Room" to start a new collaborative session. Share the Room ID with others.
   - Click "Join Room" to enter an existing Room ID.

4. **Collaborate**
   - Edit code, provide input, and run programs. All changes and outputs are synchronized in real-time.

5. **File Operations**
   - Use the File menu or keyboard shortcuts to create, open, save, or save as files.

6. **Language Selection**
   - Choose Python, C, or Java from the language dropdown before running code.

7. **Timer**
   - Use the timer controls to track coding sessions.

## Keyboard Shortcuts

- **New File:** Ctrl+N
- **Open File:** Ctrl+O
- **Save File:** Ctrl+S
- **Save As:** Ctrl+Shift+S
- **Exit:** Ctrl+Q
- **Run Code:** F5

## Notes

- The server runs locally. All users must be on the same machine or network (with port forwarding).
- Only basic user list functionality is present (UI placeholder).
- For C and Java, ensure compilers are installed and available in PATH.

## Troubleshooting

- **Tkinter Import Error:** Install Tkinter via your OS package manager.
- **Compiler Not Found:** Ensure `gcc`, `g++`, `gdb`, and `javac` are installed and in PATH.
- **Port Already in Use:** Change the port in the code if 12345 is occupied.



*Developed by Binit Kumar Shaw. Contributions welcome!*
