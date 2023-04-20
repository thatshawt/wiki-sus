from flaskr.backend import Backend, UniquePageVisit
from datetime import datetime
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from flaskr.user_list import User_List
from flaskr.user import User
from os import remove
from io import BytesIO


# TODO(Project 1): Write tests for Backend methods.
class TestBackend(unittest.TestCase):

    def test_login_wrong(self):

        # Creating temp file with hashed password
        with open('/tmp/test.txt', 'w') as f:
            f.write(
                '341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94'
            )

        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        # Mock blob.exists
        mock_blob.exists.return_value = True  # True or False
        # Mock blob.open
        mock_blob.open.return_value = open('/tmp/test.txt', 'r')

        # Mock bucket object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Mocking userpass bucket
        backend._get_userpass_bucket = MagicMock(return_value=mock_bucket)

        # Testing argument for sign-up
        username = 'testing'
        password = 'test123456'

        hashed_password = '1b14a39b0570b9ef13e36f8525896bcbaf51de1dd1026ebf9de0b32c26e47928'

        # Mock objects for SHA256 dependency
        mock_hexdigest = MagicMock()
        mock_hexdigest.hexdigest.return_value = hashed_password

        mock_sha = MagicMock()
        mock_sha.return_value = mock_hexdigest

        # Calling sign_in function
        assert backend.sign_in(
            username, password, sha256=mock_sha
        ) == False, "If this returns True then you have the correct password/Hash"
        remove('/tmp/test.txt')

    def test_login_correct(self):

        # Creating temp file with hashed password
        with open('/tmp/test.txt', 'w') as f:
            f.write(
                '341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94'
            )

        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        # Mock blob.exists
        mock_blob.exists.return_value = True  # True or False
        # Mock blob.open
        mock_blob.open.return_value = open('/tmp/test.txt', 'r')

        # Mock bucket object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Mocking userpass bucket
        backend._get_userpass_bucket = MagicMock(return_value=mock_bucket)

        # Testing argument for sign-up
        username = 'testing'
        password = 'test12345'

        hashed_password = '341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94'

        # Mock objects for SHA256 dependency
        mock_hexdigest = MagicMock()
        mock_hexdigest.hexdigest.return_value = hashed_password

        mock_sha = MagicMock()
        mock_sha.return_value = mock_hexdigest

        # Calling sign_in function
        assert backend.sign_in(username, password,
                               sha256=mock_sha) == True, "Wrong password / HASH"
        remove('/tmp/test.txt')

    def test_sign_up(self):
        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False  # True or False
        mock_blob.open.return_value = open('/tmp/test.txt', 'w')

        # Mock bucket object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Mocking userpass bucket
        backend._get_userpass_bucket = MagicMock(return_value=mock_bucket)

        # Testing argument for sign-up
        username = 'testing'
        password = 'test12345555'

        hashed_password = '341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94'

        # Mock objects for SHA256 dependency
        mock_hexdigest = MagicMock()
        mock_hexdigest.hexdigest.return_value = hashed_password

        mock_sha = MagicMock()
        mock_sha.return_value = mock_hexdigest

        # Calling sign_up function
        backend.sign_up(username, password, sha256=mock_sha)
        with open('/tmp/test.txt', 'r') as f:
            comparison = f.read()
            assert comparison == hashed_password, "Passwords don't match"
            remove('/tmp/test.txt')

    def test_get_wiki_page(self):

        # Create temp file with test text
        with open('/tmp/temp.txt', 'w') as f:
            f.write('test text')

        # Backend object instance
        backend = Backend()

        # Blob mock object
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True  # True or False
        mock_blob.open.return_value = open('/tmp/temp.txt', 'r')

        # Bucket mock object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Patching get_content_bucket function to return mock_bucket
        backend._get_content_bucket = MagicMock(return_value=mock_bucket)

        # Asserting if reading the file will give the expected result
        assert backend.get_wiki_page('temp') == 'test text'
        remove('/tmp/temp.txt')

    # This works for both user and content bucket
    @patch('flaskr.backend.storage')
    def test_get_buckets(self, mock_storage):

        # Mock bucket object
        mock_bucket = MagicMock()

        # Mock client object
        mock_client = MagicMock()
        # Client bucket returns a mock bucket
        mock_client.bucket.return_value = mock_bucket

        # Mock storage returns a mock client
        mock_storage.Client.return_value = mock_client

        backend = Backend()

        # Function call to verify it gets a bucket back
        assert backend._get_userpass_bucket(
        ) == mock_bucket, "Did not get bucket back"

    def test_get_image_0(self):

        image_data = "arbitrary_data"

        # mock.bucket().blob().open().__enter__().read().decode()

        backend = Backend()

        backend.storage_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_open = MagicMock()
        mock_enter = MagicMock()
        mock_read = MagicMock()

        backend.storage_client.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        mock_blob.open.return_value = mock_open
        mock_open.__enter__.return_value = mock_enter
        mock_enter.read.return_value = mock_read

        mock_read.decode.return_value = "arbitrary_data"

        return_value = backend.get_image("some_image")
        assert return_value == image_data

        # UNIT TESTS for user_list #

    def test_user_list_start_queue(self):
        # Instance of User_List
        user_list = User_List()

        # Expectend length result
        expected = 50

        assert len(user_list.available_nums_q) == expected

    def test_update_user_list(self):
        # Instance of User_List
        user_list = User_List()

        # Updating user_list with two users
        user_list.update_list('admin')
        user_list.update_list('root')

        # Expected results
        expected1 = {'admin': '1', 'root': '2'}
        expected2 = {'1': User('1', 'admin'), '2': User('2', 'root')}
        assert user_list.active_sessions == expected1
        assert user_list.users_dictionary == expected2

    def test_retrieve_user(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected outcome
        expected = User('1', 'admin')

        assert user_list.retrieve_user(1) == expected

    def test_change_user_id(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected outcome
        expected = {'admin': '2'}
        user_list.change_user_id('1')

        assert user_list.active_sessions == expected

    def test_change_user_id_not_found(self):

        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected outcome
        expected = 'error'

        assert user_list.change_user_id('3') == expected

    def test_remove_user_from_session(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected variables
        expected1 = 1
        expected2 = 0

        assert len(user_list.active_sessions) == expected1
        assert len(user_list.users_dictionary) == expected1

        user_list.remove_user_from_session('1')
        assert len(user_list.active_sessions) == expected2
        assert len(user_list.users_dictionary) == expected2

    def test_get_active_users(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected outcome
        expected = {'1': User('1', 'admin')}

        assert user_list.users_dictionary == expected

    def test_get_available_ids(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        expected = 49

        assert len(user_list.available_nums_q) == expected

    def test_get_active_sessions(self):
        # Instance of User_List
        user_list = User_List()

        # Updating list with a user
        user_list.update_list('admin')

        # Expected outcome
        expected = {'admin': '1'}

        assert user_list.active_sessions == expected

    def test_get_categories(self):

        # Backend object instance
        backend = Backend()

        # Blob mock object
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True  # True or False
        
        #Bucket mock object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Patching get_content_bucket function to return mock_bucket
        backend._get_content_bucket = MagicMock(return_value=mock_bucket)

        #Mocking a file
        
        fake_file = 'Crewmate,Crewmate,Tasks,Emergency Meeting\n\
                                            Imposter,Emergency Meeting,Kill,Sabotage,Sus,Venting\n\
                                            Task,Tasks\n\
                                            Location,Security,Emergency Meeting\n\
                                            Terminology,Sus,Venting\n'

        with open('/tmp/test.csv', 'w') as file:
            file.write(fake_file)

        mock_blob.open.return_value = open('/tmp/test.csv', 'r')

        


        #Expected value
        expected = {
            "Crewmate" : {"Crewmate", "Tasks", "Emergency Meeting"},
            "Imposter" : {"Emergency Meeting", "Kill", "Sabotage", "Sus", "Venting"},
            "Task"    : {"Tasks"},
            "Location" : {"Security", "Emergency Meeting"},
            "Terminology" : {"Sus", "Venting"}
        }
        
        #backend.save_categories(expected)
        actual = backend.get_categories()
        assert actual == expected 
        remove('/tmp/test.csv')


    #TODO: Implement test
    def test_save_categories(self):
        categories = {
            "Crewmate" : {"Crewmate", "Tasks", "Emergency Meeting"},
            "Imposter" : {"Emergency Meeting", "Kill", "Sabotage", "Sus", "Venting"},
            "Task"    : {"Tasks"},
            "Location" : {"Security", "Emergency Meeting"},
            "Terminology" : {"Sus", "Venting"}
        }

        # Backend object instance
        backend = Backend()

        # Blob mock object
        mock_blob = MagicMock()
        mock_blob.exists.return_value = True  
        
        #Bucket mock object
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Patching get_content_bucket function to return mock_bucket
        backend._get_content_bucket = MagicMock(return_value=mock_bucket)

        #Expected file to be "saved"
        expected = "Crewmate,Emergency Meeting,Tasks,Crewmate\nImposter,Kill,Emergency Meeting,Sabotage,Venting,Sus\nTask,Tasks\nLocation,Emergency Meeting,Security\nTerminology,Venting,Sus\n"
        

        
        #mocking a file
        open('/tmp/test.csv', 'w')

        mock_blob.open.return_value = open('/tmp/test.csv', 'w')

        backend.save_categories(categories)
        
        output = ""
        with open('/tmp/test.csv', 'r') as file:
            output = file.read()
        outputLst = output.splitlines()
        expectedLst = expected.splitlines()

        #Iterate through the input and output list, checking that the first word of each line matches
        for i in range(len(outputLst) - 1):
            outputLine = outputLst[i]
            expectedLine = expectedLst[i]
            outputItems = outputLine.split(',')
            expectedItems = expectedLine.split(',')
            for j in range(len(outputItems) - 1):
                if j == 0:
                    assert outputItems[j] == expectedItems[j]
                else:
                    assert outputItems[j] in expectedItems 
        remove('/tmp/test.csv')



        


    def test_create_message(self):
        backend = Backend()

        # Sender user object
        sender = User(1, "Joe")
        # Receiver user object
        receiver = User(2, "Mike")
        # Message to send
        message = 'Hey Mike!'

        backend.create_message(message, sender, receiver)
        
        # Expected result
        expected = 'Hey Mike!'
        assert receiver.get_message_list()['Joe'][0].get_message() == expected

    def test_get_user_messages(self):

        backend = Backend()

        # Sender user object
        sender = User(1, "Joe")
        # Receiver user object
        receiver = User(2, "Mike")

        # Add message to the message list
        receiver.append_message("Hey", sender)

        # Expected outcome
        expected = receiver.message_list

        assert backend.get_user_message_list(receiver) == expected

    # decode to json works
    def test__unique_page_visit_json_decode(self):
        visit_left = UniquePageVisit("fottnite", "127.0.0.1", datetime.fromisoformat("2023-04-20T07:39:26.620759"))
        visit_right = UniquePageVisit.decode_from_json(b'{"post_title": "fottnite", "ip": "127.0.0.1", "date": "2023-04-20T07:39:26.620759"}')

        assert visit_left == visit_right

    # encode from json works
    def test__unique_page_visit_json_encode(self):
        visit = UniquePageVisit("fottnite", "127.0.0.1", datetime.fromisoformat("2023-04-20T07:39:26.620759"))
        the_json = visit._encode_to_json()
        assert the_json == r'{"post_title": "fottnite", "ip": "127.0.0.1", "date": "2023-04-20T07:39:26.620759"}'

    # UniquePageVisit.from_ip date not within 30 days -> exists_in_past_30_days return false
    @patch("flaskr.backend.UniquePageVisit.from_ip")
    def test__not_within_30_days(self, fromIpMock):
        past30_date = datetime.fromisoformat("1876-04-20T07:39:26.620759")
        past30_visit = UniquePageVisit("fottnite", "127.0.0.1", past30_date)
        fromIpMock.return_value = past30_visit

        assert UniquePageVisit.exists_in_past_30_days(None, None, None) == False

    # UniquePageVisit.from_ip date within 30 days -> exists_in_past_30_days return true
    @patch("flaskr.backend.UniquePageVisit.from_ip")
    def test__within_30_days(self, fromIpMock):
        within30_date = datetime.now()
        within30_visit = UniquePageVisit("fottnite", "127.0.0.1", within30_date)
        fromIpMock.return_value = within30_visit

        assert UniquePageVisit.exists_in_past_30_days(None, None, None) == True

if __name__ == '__main__':
    unittest.main(verbosity=2)
