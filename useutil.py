import os, os.path, re

use_pattern = re.compile('\s*use\([\'"](?P<name>[^\'"\)]+)[\'"]\)')
use_start_pattern = re.compile('\s*use\([\'"]')
js_syntax_pattern = re.compile('JavaScript')

def search(filename):
    current_dir = os.path.dirname(filename)
    drive = os.path.splitdrive(filename)[0]
    while current_dir != '/' and current_dir != drive:
        result = search_dir(current_dir)
        if result != False:
            return result
        current_dir = os.path.dirname(current_dir)
    return False

def search_dir(dirpath):
    items = os.listdir(dirpath)
    for item in items:
        itempath = os.path.join(dirpath, item)
        if os.path.isfile(itempath) and item == 'use.json':
            return itempath
    return False

def parse_use_import_name(line):
    match = re.search(use_pattern, line)
    if (match != None):
        return match.group('name')
    return False

def get_abs_filepath(relative_path, use_json_path):
    root_dir = os.path.dirname(use_json_path)
    norm_rel_path = os.path.normpath(relative_path) + '.js'
    abs_path = os.path.join(root_dir, norm_rel_path)
    if (os.path.exists(abs_path) and os.path.isfile(abs_path)):
        return abs_path
    return False

def get_root_dir(filepath):
    return os.path.dirname(filepath)

def get_new_use_file_path(rootdir):
    return os.path.join(rootdir, 'use.json')

def is_javascript_syntax(syntax):
    basenm = os.path.basename(syntax)
    m = re.search(js_syntax_pattern, basenm)
    if (m != None):
        return True
    return False

def is_use_start(prefix):
    match = re.search(use_start_pattern, prefix)
    if (match != None):
        return True
    return False

