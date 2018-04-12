# Restaurant API

## About
Internal service for employees which help them to make a decision on lunch place. Each restaurant will be uploading menus using the system every day over API and employees will vote for menu before leaving for lunch.

## URLs
(Restaurant, '/restaurants')  POST <br>
(RestaurantList, '/restaurants/<int:id>')  GET <br>
(Employee, '/employees')  POST <br>
(EmployeeList, '/employees/<int:id>')  GET <br>
(Menu, '/restaurants/menus')  POST <br>
(TodayMenu, '/menus')  GET <br>
(GiveVote, '/menus/<int:id>/votes')  PUT <br>
(Vote, '/votes')  GET <br>
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
