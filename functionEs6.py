import sublime
import sublime_plugin


class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")
		contents = self.view.substr(sublime.Region(0, self.view.size()))
		# self.view.insert(edit, 0, contents)
		print(contents)