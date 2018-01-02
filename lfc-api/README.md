# Requirements

- `sudo apt install python-pip`
- `pip install django`
- `pip install djangorestframework`
- `pip install pygments`

# How to run
- Create an environment with the command `virtualenv -p python3 envname`
- Activate the environment `source envname_path/bin/activate`
- Go into the directory lfc-api/LookingForConcerts in our repository
- Install the requirements `pip install -r requirements.txt`
- Run the server `python manage.py runserver`

# How to test
- Go into the directory lfc-api/LookingForConcerts in our repository
- Run the command `python manage.py test lfc_backend/`
