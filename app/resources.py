from flask_restful import Resource, reqparse
from datetime import datetime

from app.models import EmployeeModel
from app.models import RestaurantModel
from app.models import MenuModel
from app.models import get_result
from app.models import get_today_date


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='This field cannot be left blank!'
    )

    def post(self):
        request_data = Employee.parser.parse_args()
        emp = EmployeeModel(**request_data)
        try:
            emp.save_to_db()
        except:
            {'message': 'An error occured inserting the employee.'}, 500 # Internal server error
        return emp.json(), 201

class EmployeeList(Resource):
    # def get(self):
    #    return {'employees': [emp.json() for emp in EmployeeModel.query.all()]}

    def get(self, id):
        emp = EmployeeModel.find_by_id(id)
        if emp:
            return emp.json()
        return {'message': 'Employee not found'}, 404

    def delete(self, id):
        emp = EmployeeModel.find_by_id(id)
        if emp:
            emp.delete_from_db()
        return {'message': 'Employee deleted'}


class Menu(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items',
        type=str,
        required=False,
        help='This field cannot be left blank!'
    )
    parser.add_argument('vote',
        type=int,
        required=False,
        help='This field cannot be left blank!'
    )
    parser.add_argument('restaurant_id',
        type=int,
        required=False,
        help='This field cannot be left blank!'
    )
    parser.add_argument('menu_date',
        type=str,
        required=False,
        help='This field cannot be left blank!'
    )

    def post(self):
        request_data = Menu.parser.parse_args()
        menu = MenuModel(**request_data)
        try:
            menu.save_to_db()
        except:
            {'message': 'An error occured inserting the menu.'}, 500
        return menu.json(), 201


class GiveVote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('vote',
        type=int,
        required=False,
        help='This field cannot be left blank!'
    )

    def put(self, id):
        request_data = GiveVote.parser.parse_args()
        menu = MenuModel.find_by_id(id) 
        menu.vote = request_data['vote']
        menu.save_to_db()
        return menu.json(), 201


class TodayMenu(Resource):
    def get(self):
        return {'menus': [menu.json() for menu in MenuModel.query.filter_by(menu_date=get_today_date()).all()]}


class Restaurant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='This field cannot be left blank!'
    )

    def post(self):
        request_data = Restaurant.parser.parse_args()
        restaurant = RestaurantModel(**request_data)
        try:
            restaurant.save_to_db()
        except:
            {'message': 'An error occured inserting the restaurant.'}, 500 # Internal server error
        return {'message': 'Restaurant created successfully.'}, 201


class RestaurantList(Resource):
    # def get(self):
    #     return {'restaurants': [restaurant.json() for restaurant in RestaurantModel.query.all()]}

    def get(self, id):
        res = RestaurantModel.find_by_id(id)
        if res:
            return res.json()
        return {'message': 'Restaurant not found'}, 404

    def delete(self, id):
        res = RestaurantModel.find_by_id(id)
        if res:
            res.delete_from_db()
        return {'message': 'Restaurant deleted'}


def json(to_dict):
    return {'name': to_dict[0], 'items': to_dict[1], 'vote': to_dict[2]}


class Vote(Resource):
    def get(self):
        return {'votes': [json(vote) for vote in get_result()]}