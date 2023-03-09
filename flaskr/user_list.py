from flaskr.user import User
from flaskr.backend import Backend
from collections import deque

# User_List class for managing website user's active sessions

class User_List:
    def __init__(self): 
        # Initializes an empty dictionary for storing all user sessions
        # { ID : USER_OBJECT}
        self.users_dictionary = {}

        # Queue for available IDs
        self.available_nums_q = self.start_available_q()

        # Dictionary of active sessions
        # (USERNAME : ID)
        self.active_sessions = {}

        # TODO Maybe implement a fix for what to do if it reaches 50 active sessions.


    # Creates a queue for a total of up to 50 simultaneous sessions of users with IDs (1 - 50)
    def start_available_q(self):
        empty_q = deque()
        for i in range(1, 51):
            empty_q.append(str(i))
        return empty_q

    def update_list(self, username): # Receives username after being verified by backend sign_in

        if username in self.active_sessions:
            active_session_id = self.active_sessions.get(username)
            return self.users_dictionary.get(active_session_id)

        # An available ID is retrieved from the queue
        # And it is added to the users_dictionary { ID : USER_OBJECT}
        user_id = self.available_nums_q.popleft()
        self.users_dictionary[user_id] = User(user_id, username)


        # Adds username to an active session dictionary
        # This will allow for efficient use of those 50 sessions
        # And avoid duplicates
        # active_sessions = { username : user_id }
        self.active_sessions[username] = user_id

        return self.users_dictionary.get(user_id)

    def retrieve_user(self, user_id):
        return self.users_dictionary.get(str(user_id))

    

    # change_user_id will be used for when user decides to change password.
    # It will allow for changing a session's ID which will cause
    # User to be logged out everywhere.

    def change_user_id(self, old_id):

        # verifies if this ID exists
        if old_id not in self.users_dictionary:
            return 'error'

        # Pops the user from the users_dictionary
        # Gets an available ID from the queue
        user_object = self.users_dictionary.pop(old_id)
        current_id = self.available_nums_q.popleft()

        # Update user ID
        user_object.new_id(current_id)

        # Adds user to the dictionary with a new ID
        # Updates the active_sessions ID with the new one
        self.users_dictionary[current_id] = user_object
        self.active_sessions[user_object.username] = current_id

 
        # Adds the old one to the queue of available IDs
        self.available_nums_q.append(old_id)

    
    # Function for removing user from active sessions
    def remove_user_from_session(self, user_id):
        # Pop user from the users_dictionary
        user_object = self.users_dictionary.pop(user_id)

        # Adds the ID to the stack of available numbers
        self.available_nums_q.append(user_id)

        # Removes the username from the active_sessions dictionary
        self.active_sessions.pop(user_object.username)

    def get_active_users(self):
        return self.users_dictionary

    def get_available_ids(self):
        return str(self.available_nums_q)
    
    def get_active_sessions(self):
        return self.active_sessions


    # Function for TESTING/DEBUGGING purposes
    def poblate_users(self):
        test = Backend()
        lst = test.test()
        for element in lst:
            self.update_list(element)