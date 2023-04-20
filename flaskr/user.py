from flask_login import UserMixin
from flaskr.message import Message
from collections import defaultdict

class User(UserMixin):

    def __init__(self, id, username):
        self.id = str(id)
        self.username = username
        # message dictionary -> {AUTHOR : list of MESSAGE objects}
        self.message_list = defaultdict(list)
        self._is_admin = False

        if username == 'admin':
            self._is_admin = True

    def new_id(self, new_id):
        self.id = new_id

    # Message : str and sender_user : User object
    def append_message(self, message, sender_user):
        message_object = Message(sender_user, message)
        self.message_list[sender_user].append(message_object)

    def get_message_list(self):
        return self.message_list