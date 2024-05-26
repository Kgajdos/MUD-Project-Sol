class Book:
    def __init__(self, title):
        self.title = title
        self.pages = []

    def add_page(self, number, text):
        self.pages.append(Page(number, text))

    def get_page(self, number):
        return next((page for page in self.pages if page.number == number), None)

class Page:
    def __init__(self, number, text):
        self.number = number
        self.text = text
