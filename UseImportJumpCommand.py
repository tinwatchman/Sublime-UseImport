import sublime, sublime_plugin
import json
import useutil

class UseImportJumpCommand(sublime_plugin.TextCommand):
    def description(self):
        return 'Jump to File (Use-Import)'

    def is_enabled(self):
        return self.is_javascript_view()
        
    def is_visible(self):
        return self.is_javascript_view() and self.is_use_import_name()

    def run(self, edit):
        if self.is_javascript_view():
            name = self.find_use_import_name()
            if (name != False):
                data = self.get_config()
                if name in data:
                    relpath = data.get(name)
                    configpath = self.view.settings().get('UseImport_use_json_path')
                    abspath = useutil.get_abs_filepath(relpath, configpath)
                    if abspath != False:
                        self.view.window().open_file(abspath)

    def is_javascript_view(self):
        file_syntax = self.view.settings().get('syntax')
        return useutil.is_javascript_syntax(file_syntax)

    def is_use_import_name(self):
        sels = self.view.sel()
        for sel in sels:
            curline = self.view.substr(self.view.line(sel))
            m = useutil.parse_use_import_name(curline)
            if (m != False):
                return True
        return False

    def find_use_import_name(self):
        sels = self.view.sel()
        for sel in sels:
            curline = self.view.substr(self.view.line(sel))
            m = useutil.parse_use_import_name(curline)
            if (m != False):
                return m
        return False

    def get_config(self):
        if self.view.settings().has('UseImport_use_json_path'):
            filepath = self.view.settings().get('UseImport_use_json_path')
        else:
            filepath = useutil.search(self.view.file_name())
            self.view.settings().set('UseImport_use_json_path', filepath)
        if filepath != False:
            return self.load_file(filepath)
        return False

    def load_file(self, filepath):
        with open(filepath, 'r') as myfile:
            rawdata = myfile.read()
        return json.loads(rawdata)
