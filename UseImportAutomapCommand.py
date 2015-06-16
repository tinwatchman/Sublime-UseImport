import sublime, sublime_plugin
import os
import useutil

class UseImportAutomapCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.is_javascript_view(self.view)
        
    def is_visible(self):
        return self.is_javascript_view(self.view)

    def run(self, edit):
        if self.is_javascript_view(self.view):
            # delete stored settings
            self.clear_preferences()
            # get use file location
            configpath = useutil.search(self.view.file_name())
            print "configpath found: %s" % configpath
            if (configpath == False):
                rootdir = useutil.get_root_dir(self.view.file_name())
                configpath = useutil.get_new_use_file_path(rootdir)
            else:
                rootdir = useutil.get_root_dir(configpath)
            args = {
                "cmd": [
                    "use-automapper",
                    "run",
                    "--path",
                    useutil.replace_back_slashes(rootdir),
                    "--output",
                    useutil.replace_back_slashes(configpath)
                ]
            }

            if sublime.platform() == "osx":
                args['path'] = "/usr/local/share/npm/bin:/usr/local/bin:/opt/local/bin"
            
            self.view.window().run_command('exec', args)
        return

    def is_javascript_view(self, view):
        file_syntax = view.settings().get('syntax')
        return useutil.is_javascript_syntax(file_syntax)

    def clear_preferences(self):
        views = self.view.window().views()
        for view in views:
            if self.is_javascript_view(view) and view.settings().has('UseImport_use_json_path'):
                view.settings().erase('UseImport_use_json_path')
        return
