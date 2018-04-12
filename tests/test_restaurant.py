import unittest
import json

from app import create_app, db


class RestaurantTestCase(unittest.TestCase):
    '''This class represents the restaurant test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.restaurant = {'name': 'test_name'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_restaurant_creation(self):
        '''Test API can create a restaurant (POST request)'''
        res = self.client().post('/restaurants', data=self.restaurant)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Restaurant created successfully', str(res.data.decode('utf-8')))

    def test_api_can_get_restaurant_by_id(self):
        '''Test API can get a single restaurant by using it's id.'''
        rv = self.client().post('/restaurants', data=self.restaurant)
        self.assertEqual(rv.status_code, 201)
        result = self.client().get('/restaurants/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('test_name', str(result.data))

    def test_restaurant_deletion(self):
        '''Test API can delete an existing restaurant. (DELETE request).'''
        rv = self.client().post(
            '/restaurants',
            data={'name': 'test_name'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/restaurants/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/restaurants/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        '''teardown all initialized variables.'''
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()