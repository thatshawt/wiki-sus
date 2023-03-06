from flaskr.backend import Backend
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from os import remove

# TODO(Project 1): Write tests for Backend methods.
class TestBackend(unittest.TestCase):

    def test_login_wrong(self):

        # Creating temp file with hashed password
        with open('/tmp/test.txt', 'w') as f:
            f.write('341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94')

        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        # Mock blob.exists
        mock_blob.exists.return_value = True # True or False
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
        assert backend.sign_in(username, password, sha256=mock_sha) == False , "If this returns True then you have the correct password/Hash"
        remove('/tmp/test.txt')

    def test_login_correct(self):

        # Creating temp file with hashed password
        with open('/tmp/test.txt', 'w') as f:
            f.write('341983e50d13e2bc60b349883f5fe5bcd8aba2ba94b5aef41c763c3642e9fd94')

        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        # Mock blob.exists
        mock_blob.exists.return_value = True # True or False
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
        assert backend.sign_in(username, password, sha256=mock_sha) == True , "Wrong password / HASH"
        remove('/tmp/test.txt')
        


    def test_sign_up(self):
        # Create backend object
        backend = Backend()

        # A mock blob object
        mock_blob = MagicMock()
        mock_blob.exists.return_value = False # True or False
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
        mock_blob.exists.return_value = True # True or False
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
        assert backend._get_userpass_bucket() == mock_bucket, "Did not get bucket back"

    @patch('flaskr.backend.storage')
    def test_get_image(self, mock_storage):
        B64 = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
        # B64 Image
        with open('/tmp/test.txt', 'w') as f:
            f.write(B64)
        
        # Mock object for base64 dependency
        mock_base64 = MagicMock()
        mock_base64.b64encode.return_value = B64.encode('utf-8')
       

        # Mock object for blob
        mock_blob = MagicMock()
        mock_blob.open.return_value = open('/tmp/test.txt', 'r')
        
        # Mock object for bucket
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob

        # Mock object for client
        mock_client = MagicMock()
        mock_client.bucket = mock_bucket

        mock_storage.Client.return_value = mock_client

        backend = Backend()
        
        assert backend.get_image(filename='hello.txt', base64=mock_base64) == B64


if __name__ == '__main__':
    unittest.main(verbosity=2)
   