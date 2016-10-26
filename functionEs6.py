import sublime
import sublime_plugin

# The script allows you to add a new function (ES6 style) by
# selecting the function signiture name and press ctrl+shift+E 
# or by right click on the selected are and choose ES6 Function.
# The script also add automatic 'this.' to the signiture and pass parameters.

TAB = '\t'
NEW_LINE = '\n'
CLOSE_BRACKET = '}'
ARROW_FUNCTION_BUILDER_FIRST_PART = ' = ('
ARROW_FUNCTION_BUILDER_SECOND_PART = ') => {\n\n\t}\n'

class funcToEs6Command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		window = view.window()
		function_parameters =''
		end_of_class = self.get_end_of_class()		
		self.selectedText = self.get_selected_text()

		if not self.is_selected_text_exist(self.selectedText+' =', self.selectedText+'='):
			temp_selected_text = self.selectedText
			# Check if the function contains parameters to pass
			if '(' in self.selectedText:
				self.selectedText, braces = self.selectedText.split('(')
				function_parameters = braces.split(')')[0].replace(',',', ')
			# Check that the selected text is not empty
			if self.selectedText is not '':
				edited_function_name = NEW_LINE + TAB + self.selectedText + ARROW_FUNCTION_BUILDER_FIRST_PART + function_parameters + ARROW_FUNCTION_BUILDER_SECOND_PART + self.view.substr(end_of_class)
				self.view.replace(edit, end_of_class, edited_function_name)
				self.rename_function(temp_selected_text)

	def get_end_of_class(self):
		'''find the end of class'''
		all_matches = self.view.find_all(CLOSE_BRACKET)
		return all_matches[len(all_matches) -1]
	
	def get_selected_text(self):
		'''get the selected text'''
		sel = self.view.sel()
		selectedRegions = sel[0]
		return self.view.substr(selectedRegions)
	
	def rename_function(self, selectedText):
		'''Add "this." if not exist '''
		if not selectedText.startswith('this.'):
			selectedTextWithPrefix = 'this.' + selectedText	
			self.view.run_command("insert",{"characters": selectedTextWithPrefix})

	def is_selected_text_exist(self, *args):
		''' check if function already exist in file '''
		for arg in args:
			is_exist = self.view.find_all(arg) == []
			if not is_exist:
				sublime.message_dialog("Function name already exist OR Empty")
				return True
		return False

