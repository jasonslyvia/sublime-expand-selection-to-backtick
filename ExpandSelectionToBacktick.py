import sublime, sublime_plugin

# Inspired by: https://github.com/kek/sublime-expand-selection-to-quotes

class ExpandSelectionToBacktickCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		e_quotes = list(map(lambda x: x.begin(), self.view.find_all("`")))

		for sel in self.view.sel():
			def search_for_quotes(q_type, quotes):
				q_size, before, after = False, False, False

				if len(quotes) - self.view.substr(sel).count('"') >= 2:
					all_before = list(filter(lambda x: x < sel.begin(), quotes))
					all_after = list(filter(lambda x: x >= sel.end(), quotes))

					if all_before: before = all_before[-1]
					if all_after: after = all_after[0]

					if all_before and all_after: q_size = after - before

				return q_size, before, after

			e_size, e_before, e_after = search_for_quotes("`", e_quotes)

			def replace_region(start, end):
				if sel.size() < end-start-2:
					start += 1; end -= 1
				self.view.sel().subtract(sel)
				self.view.sel().add(sublime.Region(start, end))

			if e_size:
				replace_region(e_before, e_after+1)
