import sublime, sublime_plugin
import json
import useutil

class UseImportCompletionListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if self.is_javascript_view(view) and self.is_use_start(view):
            data = self.get_config(view)
            if (data != False):
                matches = []
                charmatches = []
                others = []
                results = []
                pre = prefix.strip().lower()
                names = data.keys()
                for name in names:
                    formatname = name.strip().lower()
                    if pre in formatname:
                        matches.append(self.get_autosuggestion(name))
                    elif pre[0] == formatname[0]:
                        charmatches.append(self.get_autosuggestion(name))
                    else:
                        others.append(self.get_autosuggestion(name))
                results.extend(matches)
                results.extend(charmatches)
                results.extend(others)
                return (results, sublime.INHIBIT_WORD_COMPLETIONS)
        return None

    def is_javascript_view(self, view):
        file_syntax = view.settings().get('syntax')
        return useutil.is_javascript_syntax(file_syntax)

    def is_use_start(self, view):
        sels = view.sel()
        for sel in sels:
            curline = view.substr(view.line(sel))
            m = useutil.is_use_start(curline)
            if (m != False):
                return True
        return False

    def get_config(self, view):
        if view.settings().has('UseImport_use_json_path'):
            filepath = view.settings().get('UseImport_use_json_path')
        else:
            filepath = useutil.search(view.file_name())
            view.settings().set('UseImport_use_json_path', filepath)
        if filepath != False:
            return self.load_file(filepath)
        return False

    def load_file(self, filepath):
        with open(filepath, 'r') as myfile:
            rawdata = myfile.read()
        return json.loads(rawdata)

    def get_autosuggestion(self, name):
        return ( name + '\t (UseImport)', name )

