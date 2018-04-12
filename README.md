# Restaurant API

## About
Internal service for employees which help them to make a decision on lunch place. Each restaurant will be uploading menus using the system every day over API and employees will vote for menu before leaving for lunch.

## URLs
(Restaurant, '/restaurants')  POST
(RestaurantList, '/restaurants/<int:id>')  GET
(Employee, '/employees')  POST
(EmployeeList, '/employees/<int:id>')  GET   
(Menu, '/restaurants/menus')  POST
(TodayMenu, '/menus')  GET
(GiveVote, '/menus/<int:id>/votes')  PUT
(Vote, '/votes')  GET
<br>
Automated tests (python mangage.py test)<br>
Logging (app.log)<br>
<br>
## Installation
```
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-RESTful

python mangage.py test
python run.py
```