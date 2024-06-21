from cx_Freeze import setup, Executable

# Define the executable and the files to be included
executables = [Executable("main.py", base=None)]

# Define the setup options
setup(
    name="MainScript",
    version="1.0",
    description="My Python Script",
    executables=executables,
)
