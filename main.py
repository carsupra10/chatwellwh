import subprocess

# Define the paths to your Python scripts
script_paths = ['chatbot.py', 'bot4.py']

# Loop through each script and run it using subprocess
for script_path in script_paths:
    subprocess.run(['python', script_path])
