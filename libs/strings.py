"""
libs.strings

Library to access for translations for different strings stored the <project-root>/strings folder
file should json and file name should be the locale name.

By default strings/en-gb.json will be used. assign different locale to libs.strings.default_locale to load the corresponding file.
make sure to call libs.strings.refresh() to use the load the newly mentioned file.

"""
import json
import os

default_locale = 'en-gb'
cached_strings = {}

def refresh():
    """ Loads the json file from the given path and caches it's content. """
    global cached_strings
    curr_dir = os.getcwd()
    with open(f"{curr_dir}/strings/{default_locale}.json") as file:
        cached_strings = json.load(file)

def gettext(name:str) -> str:
    """ To access a string from the loaded file with 'name' as key. """
    return cached_strings[name]

refresh()