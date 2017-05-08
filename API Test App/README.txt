Assuming that you have pip, install django as follows:
pip install django
pip install djangorestframework
pip install pygments
After these installations 

Create a folder to copy the branch.
Clone the repository: git clone https://github.com/bounswe/bounswe2017group2.git ~/Desktop/ConcertAPI
Go into the folder: ConcertAPI
All the required, most recent files are there.

Move into the folder of the api: cd "ConcertAPI"
Yes we have 2 concerts API folders consecutively
Activate the environment: source env/bin/activate
Go into the ConcertAPI folder: cd ConcertAPI
Run the server: python manage.py runserver

See the Concerts lists by going to the address "http://127.0.0.1:8000/concert/"
See the Users lists by going to the adress "http://127.0.0.1:8000/user/"

Post new concert by typing: "http --json POST http://127.0.0.1:8000/concert/ artist="Sezen Aksu", location = "Istanbul", date = "2017-10-10", minPrice = 100, maxPrice = 300"
Post new user by typing "http --json POST http://127.0.0.1:8000/user/" posting json file by writing "http://127.0.0.1:8000/users/ name="Ali", email = "aliveli@mail.com", password = "aosjd123", age = 23"
