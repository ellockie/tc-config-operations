import configparser
from collections import defaultdict
from io import StringIO


class MultiValueDict(dict):
    def __setitem__(self, key, value):
        if key in self and isinstance(self[key], list):
            self[key].append(value)
        else:
            super(MultiValueDict, self).__setitem__(key, [value])


class MultiValueConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        kwargs['dict_type'] = MultiValueDict
        super(MultiValueConfigParser, self).__init__(*args, **kwargs)


# Load the wincmd.ini file
with open('wincmd.ini', 'r') as f:
    ini_data = f.read()

# Read the ini data and sort sections
config = MultiValueConfigParser()
config.read_string(ini_data)
sorted_sections = sorted(config.sections())

# Sort lines within each section
output = StringIO()
for section in sorted_sections:
    output.write(f'[{section}]\n')
    sorted_keys = sorted(config[section].keys())
    for key in sorted_keys:
        for value in config[section][key]:
            output.write(f'{key}={value}\n')
    output.write('\n')

# Save the sorted ini data to a new file
with open('sorted_wincmd.ini', 'w') as f:
    f.write(output.getvalue())

output.close()
print("File sorted_wincmd.ini created with sorted contents.")
