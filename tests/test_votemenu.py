import unittest
import json

from app import create_app, db


from app.models import get_today_date


class MenuVoteTestCase(unittest.TestCase):
    '''This class represents the bucketlist test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.restaurant = {'name': 'test_restaurant'}
        self.menu = {'items': 'Meat, Water', 'vote': 0, 'restaurant_id': 1, 'menu_date': get_today_date()}
        self.vote = {'vote': 5}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_menu_creation(self):
        '''Test API can create a menu (POST request)'''
        post_res = self.client().post('/restaurants', data=self.restaurant)
        post_menu = self.client().post('/restaurants/menus', data=self.menu)
        self.assertEqual(post_res.status_code, 201)
        self.assertEqual(post_menu.status_code, 201)
        self.assertIn(str(self.menu['items']), str(post_menu.data.decode('utf-8')))

    def test_api_can_get_menus_for_today(self):
        '''Test API can get menus for today.'''
        rv = self.client().post(
            '/restaurants/menus',
            data=self.menu)
        self.assertEqual(rv.status_code, 201)
        result = self.client().get('/menus')
        self.assertEqual(result.status_code, 200)
        self.assertIn(str(self.menu['items']), str(rv.data.decode('utf-8')))

    def test_menu_add_vote(self):
        '''Test API can add vote for single menu. (PUT request)'''
        rv = self.client().post(
            '/restaurants/menus',
            data=self.menu)
        self.assertEqual(rv.status_code, 201)
        self.menu['vote'] = self.vote['vote']
        rv = self.client().put(
            '/menus/1/votes',
            data=self.menu)
        self.assertEqual(rv.status_code, 201)
        results = self.client().get('/menus')
        self.assertIn(str(self.vote['vote']), results.data.decode('utf-8'))


    def tearDown(self):
        '''teardown all initialized variables.'''
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()