from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username):
        self.id = str(id)
        self.username = username
        self._is_admin = False

        if username == 'admin':
            self._is_admin = True

    def new_id(self, new_id):
        self.id = new_id
