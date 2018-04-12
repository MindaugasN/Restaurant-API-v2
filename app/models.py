from datetime import datetime
from sqlalchemy import func

from app import db


class EmployeeModel(db.Model):
    '''This class represents the employees table.'''
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class MenuModel(db.Model):
    '''This class represents the menuus table.'''
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(200))
    vote = db.Column(db.Integer, server_default="")
    menu_date = db.Column(db.String(10))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('RestaurantModel')

    def __init__(self, items, vote, restaurant_id, menu_date):
        #self.id = id
        self.items = items
        self.vote = vote
        self.restaurant_id = restaurant_id
        self.menu_date = menu_date

    def json(self):
        return {'id': self.id, 'items': self.items, 'vote': self.vote, 'restaurant_id': self.restaurant_id, 'menu_date': self.menu_date}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class RestaurantModel(db.Model):
    '''This class represents the restaurants table.'''
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

def get_result():
    result = (
        db.session.query(
            RestaurantModel.name,
            MenuModel.items,
            func.avg(MenuModel.vote).label('average')
        )
        .filter(MenuModel.menu_date == get_today_date())
        .join(MenuModel)
        .group_by(RestaurantModel.name, MenuModel.items)
        .order_by(db.desc('average'))
    )
    return result



