import re
import os
import string
from gameParser import GameParser

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

# Read the input file
with open('OCA_2.0.pdn', 'r') as infile:
    data = infile.read()

# Ignore lines starting with '['
lines = data.split('\n')
filtered_lines = [line for line in lines if not line.startswith('[')]
filtered_data = '\n'.join(filtered_lines)

# Use regular expressions to find and remove content between '{' and '}', inclusive
pattern = r'\{[^}]*\}\s*'
modified_data = re.sub(pattern, '', filtered_data)

# Write the modified content to an output file
with open('new_OCA_2.0.pdn', 'w') as outfile:
    outfile.write(modified_data)

game_records = modified_data.split('\n\n')

for game_record in game_records:
    GameParser.parseGame(game_record.rstrip(string.whitespace))