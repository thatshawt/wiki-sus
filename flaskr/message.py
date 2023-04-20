from datetime import date, datetime
class Message:
    def __init__(self, author, message):
        self.author = author
        self.message = message
        self.date = date.today()
        self.time = datetime.now().strftime("%H:%M")

    def get_author(self):
        return self.author
    
    def get_message(self):
        return self.message