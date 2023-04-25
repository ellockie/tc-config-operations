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

FILENAME = {
    "SOURCE": "wincmd.ini",
    "TARGET": "wincmd.sorted.ini",
}
NUMBER_REGEX = re.compile(r'^([a-zA-Z_]*)(\d+)(\w*)=')


class MultiValueDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super().__init__(list, *args, **kwargs)


class MultiValueConfigParser:
    def __init__(self, ini_file):
        self.source_file = ini_file
        self.sections = {}

    def read_data(self):
        sections_added = set()
        current_section = None
        curkey = None
        lineno = -1

        for line in self.source_file:
            lineno += 1
            if not line.strip():
                continue
            if line.startswith((' ', '\t')):
                continue
            else:
                if line.startswith('['):
                    end = line.find(']')
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
                elif current_section is None:
                    raise Exception("MissingSectionHeaderError")
                else:
                    current_section.append(line.strip())


def extract_number_from_key(key, section_name):
    if section_name not in SPECIAL_SORTING_SECTIONS:
        return ''
    match = re.search(NUMBER_REGEX, key)
    result = f'{match.group(1)}_{match.group(2).rjust(10, "0")}_{match.group(3)} ::: {key}' if match else ''
    return result


with open(FILENAME["SOURCE"], 'r') as source_ini_file:
    # Read the ini data and sort sections
    config = MultiValueConfigParser(source_ini_file)
    config.read_data()

    sorted_sections = sorted(config.sections, key=lambda k: k.lower())
    print(sorted_sections)

    # Sort lines within each section
    output = StringIO()
    for cfg_section_name in sorted_sections:
        output.write(f'[{cfg_section_name}]\n')
        sorted_keys = sorted(
            config.sections[cfg_section_name],
            key=lambda k: (extract_number_from_key(k, cfg_section_name), k.lower())
        )
        for line in sorted_keys:
            output.write(f'{line}\n')
        output.write('\n')

    # Save the sorted ini data to a new file
    with open(FILENAME["TARGET"], 'w') as target_file:
        target_file.write(output.getvalue())
        output.close()

print(f'File \"{FILENAME["TARGET"]}\" created with sorted contents.')
