class Message:
    def __init__(self, author, message):
        self.author = author
        self.message = message

    def get_author(self):
        return self.author
    
    def get_message(self):
        return self.message