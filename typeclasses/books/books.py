from evennia import Command, CmdSet, EvMenu
from typeclasses.objects import Object

class CmdReadBook(Command):
	"""
	Read the book

	Usage:
		read <book name>
	"""
	key = "book"
	aliases = ["read"]
	help_category = "General"

	def func(self):
		self.obj.open_book(self.caller)

class BookCmdSet(CmdSet):
	def at_cmdset_creation(self):
		self.add(CmdReadBook())

def node_titlepage(caller, raw_string, **kwargs):
	"This is the first page of the book"

	menu = caller.ndb._evmenu
	bookname = menu.bookname
	bookkeeper = menu.bookkeeper
	pages = bookkeeper.contents

	text = f"*** {bookname} ***\n"
	if pages:
		text += f"	Go to page: {len(pages)}."
	else:
		text += "	There are no pages in this book; quit to exit."

	options = []

	for page in pages:
		options.append({"desc": (f"{page.key}"),
						"goto": ("read_page", {"selected_page": page})})

	return text, options

def node_read_page(caller, raw_string, **kwargs):
	"This opens the pages to be read"
	selected_page = kwargs["selected_page"]

	text = pages.db.desc

	options = ({"desc": "Return to title page.",
				"goto": "titlepage"})


class Book(Object):
	def open_book(self, reader):
		menunodes = {} #Be sure to add the menunodes here
		bookname = self.db.bookname or "Book"
		EvMenu(reader, menunodes, startnode = "titlepage",
		bookname = bookname, bookkeeper = self, pages = self.contents)