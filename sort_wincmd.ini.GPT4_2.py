import configparser
from collections import defaultdict
from io import StringIO


class MultiValueDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super().__init__(list, *args, **kwargs)


class MultiValueConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        kwargs['dict_type'] = MultiValueDict
        super().__init__(*args, **kwargs)

    def _read(self, fp, fpname):
        elements_added = set()
        cursect = None
        curkey = None

        for lineno, line in enumerate(fp, start=1):
            if not line.strip():
                continue
            if line.startswith((' ', '\t')):
                if curkey:
                    value = line.strip()
                    if value:
                        cursect[curkey].append(value)
            else:
                if line.startswith('['):
                    end = line.find(']')
                    if end > 0:
                        sectname = line[1:end].strip()
                        if sectname in elements_added:
                            cursect = self[sectname]
                        else:
                            cursect = self._sections[sectname] = self._dict()
                            elements_added.add(sectname)
                    else:
                        raise configparser.MissingSectionHeaderError(fpname, lineno, line)
                elif cursect is None:
                    raise configparser.MissingSectionHeaderError(fpname, lineno, line)
                else:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    cursect[key].append(value)
                    curkey = key


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
    sorted_keys = sorted(config[section])
    for key in sorted_keys:
        for value in config[section][key]:
            output.write(f'{key}={value}\n')
    output.write('\n')

# Save the sorted ini data to a new file
with open('sorted_wincmd.ini', 'w') as f:
    f.write(output.getvalue())

output.close()
print("File sorted_wincmd.ini created with sorted contents.")
