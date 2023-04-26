from flask_login import UserMixin
from flaskr.message import Message
from collections import defaultdict

class User(UserMixin):

    def __init__(self, id, username):
        self.id = str(id)
        self.username = username

        # Conversation dictionary -> {Who you're sending to -> Messages}
        self.conversations = defaultdict(list)

        self._is_admin = False

        if username == 'admin':
            self._is_admin = True

    def new_id(self, new_id):
        self.id = new_id

    # Message : str and sender_user : User object
    def sent_message(self, message, receiver_user):
        message_object = Message(self.username, message)
        self.conversations[receiver_user].append(message_object)

    # Both sent and receive methods must be called together to create a sent message for the sender
    # And the receiver to add it to the list.

    def receive_message(self, message, sender_user):
        message_object = Message(sender_user, message)
        self.conversations[sender_user].append(message_object)

    def get_conversation_list(self):
        return self.conversations