import unittest

from party import app
from model import db, example_data, connect_to_db

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///games"
class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get('/')
        self.assertNotIn('123 Magic Unicorn Way', result.data)
                
    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn('123 Magic Unicorn Way', result.data)
        self.assertNotIn('Please RSVP', result.data)

    def test_games(self):
        result = self.client.get("/games",follow_redirects=True)
        self.assertNotIn("Ticket to Ride", result.data)
        self.assertIn("You have not RSVP-ed", result.data)

class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True        

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get('/games')
        self.assertIn('Monopoly', result.data)
        self.assertIn('Scrabble', result.data)


class RSVPPartyTests(unittest.TestCase):
    """Tests for my party site RSVP."""

    def setUp(self):
        # connect_to_db(app)
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def test_games(self):
        result = self.client.get('/games')
        self.assertIn("Ticket to Ride", result.data)


if __name__ == "__main__":
    
    unittest.main()
    # connect_to_db(app)
