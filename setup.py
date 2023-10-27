from cx_Freeze import setup, Executable

# Define the list of executables (the entry points)
executables = [Executable("checkers/main.py")]

# Set up the setup parameters
setup(
    name="Checkers",
    version="1.0",
    executables=executables
)