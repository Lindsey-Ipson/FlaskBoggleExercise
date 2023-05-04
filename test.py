from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure proper HTML is rendered and proper data is in the session"""

        with self.client:
            resp = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'<button>Submit word!', resp.data)
            self.assertIn(b'<p>Your Words:</p>', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))
            self.assertEqual(resp.status_code, 200)

    def test_valid_guess(self):
        """Make sure valid guess comes back as valid"""

        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [["Z", "J", "F", "Y", "J"], 
                                 ["V", "L", "G", "H", "H"], 
                                 ["X", "V", "N", "A", "D"], 
                                 ["E", "N", "N", "V", "H"], 
                                 ["M", "A", "J", "K", "V"]]
        resp = self.client.get('/check-guess?guess=had')
        self.assertEqual(resp.json['result'], 'ok')

    def test_word_not_on_board(self):
        """Make sure guess that is real word but not on board comes back as not-on-board"""

        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [["Z", "J", "F", "Y", "J"], 
                                 ["V", "L", "G", "H", "H"], 
                                 ["X", "V", "N", "A", "D"], 
                                 ["E", "N", "N", "V", "H"], 
                                 ["M", "A", "J", "K", "V"]]
            resp = self.client.get('/check-guess?guess=nowhere')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_not_real_word(self):
        """Make sure guess that is not real word comes back as not-word"""

        self.client.get('/')
        resp = self.client.get('/check-guess?guess=qwtfuqtefd')
        self.assertEqual(resp.json['result'], 'not-word')   

            

