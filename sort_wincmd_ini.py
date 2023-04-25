import configparser
from collections import defaultdict
from io import StringIO
import re


SPECIAL_SORTING_SECTIONS = [
    "Associations",
    "Colors",
    "Command line history",
    "ContentPlugins",
    "ContentPlugins64",
    "CustomFields"
    "DirMenu",
    "LeftHistory",
    "ListerPlugins",
    "ListerPlugins64",
    "MkDirHistory",
    "NewFileHistory",
    "RenameSearchFind",
    "RenameSearchReplace",
    "RenameTemplates",
    "RightHistory",
    "SearchIn",
    "SearchName",
    "Selection",
    "Tabstops",
    "lefttabs",
    "righttabs",
    "user"
]


class MultiValueDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super().__init__(list, *args, **kwargs)


class MultiValueConfigParser:
    def __init__(self, ini_file):
        self.source_file = ini_file
        # print(f"ini_file: {len(ini_file)}")
        self.sections = {}

    def read_data(self):
        sections_added = set()
        current_section = None
        curkey = None
        lineno = -1

        # for lineno, line in enumerate(self.source_data, start=1):

        # for lineno, line in self.source_file:
        for line in self.source_file:
            lineno += 1
            if not line.strip():
                continue
            if line.startswith((' ', '\t')):
                if curkey:
                    value = line.strip()
                    if value:
                        current_section[curkey].append(value)
            else:
                # print(f"line: {lineno}: {line}")
                if line.startswith('['):
                    end = line.find(']')

                    # print(f"end: {end}")
                    if end > 0:
                        section_name = line[1:end].strip()
                        if section_name in sections_added:
                            raise Exception(f"Duplicate section Error: [{section_name}]")
                        else:
                            current_section = self.sections[section_name] = []
                            sections_added.add(section_name)
                        print(f"Section: {section_name}")
                    else:
                        raise Exception("Missing Section Header Name Error")
                        # raise configparser.MissingSectionHeaderError(fpname, lineno, line)
                elif current_section is None:
                    raise Exception("MissingSectionHeaderError")
                    # raise configparser.MissingSectionHeaderError(fpname, lineno, line)
                else:
                    current_section.append(line.strip())
                    # key, value = line.split('=', 1)
                    # key = key.strip()
                    # value = value.strip()
                    # curkey = key


def extract_number_from_key(key, section_name):
    if section_name not in SPECIAL_SORTING_SECTIONS:
        return ''
    match = re.search(r'^([a-zA-Z_]*)(\d+)(\w*)=', key)
    result = f'{match.group(1)}_{match.group(2).rjust(10, "0")}_{match.group(3)} ::: {key}' if match else ''

    # if result != '':
    #     print(result)
    return result


with open('wincmd_source.ini', 'r') as wincmd_ini_file:
    # ini_file = f.read()

    # Read the ini data and sort sections
    config = MultiValueConfigParser(wincmd_ini_file)
    config.read_data()

    sorted_sections = sorted(config.sections, key=lambda k: k.lower())
    print(sorted_sections)

    # Sort lines within each section
    output = StringIO()
    for section_name in sorted_sections:
        output.write(f'[{section_name}]\n')
        # sorted_keys = sorted(config[section])
        # print(f'config[section_name]:  {config.sections[section_name]}')
        sorted_keys = sorted(config.sections[section_name], key=lambda k: (extract_number_from_key(k, section_name), k.lower()))

        # for line in sorted(config.sections[section_name]):
        for line in sorted_keys:
            # for value in config[section][key]:
            #     output.write(f'{key}={value}\n')
            output.write(f'{line}\n')
        output.write('\n')

    # Save the sorted ini data to a new file
    with open('wincmd_sorted.ini', 'w') as f:
        f.write(output.getvalue())

        output.close()
print("File sorted_wincmd.ini created with sorted contents.")
