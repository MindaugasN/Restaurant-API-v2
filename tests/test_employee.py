import unittest
import os
import json

from app import create_app, db


class EmployeeTestCase(unittest.TestCase):
    '''This class represents the employee test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.employee = {'name': 'test_name'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_employee_creation(self):
        '''Test API can create an employee (POST request)'''
        res = self.client().post('/employees', data=self.employee)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test_name', str(res.data))

    def test_api_can_get_employee_by_id(self):
        '''Test API can get a single employee by using it's id.'''
        rv = self.client().post('/employees', data=self.employee)
        self.assertEqual(rv.status_code, 201)
        result = self.client().get('/employees/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('test_name', str(result.data))

    def test_employee_deletion(self):
        '''Test API can delete an existing employee. (DELETE request).'''
        rv = self.client().post(
            '/employees',
            data={'name': 'test_name'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/employees/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/employees/1')
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