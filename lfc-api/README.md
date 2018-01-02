# Requirements
- `sudo apt install python-pip`

# How to run
- Create an environment with the command `virtualenv -p python3 envname`
- Activate the environment `source envname_path/bin/activate`
- Go into the directory `lfc-api/LookingForConcerts` in our repository
- Install the requirements `pip install -r requirements.txt`
- Run the server `python manage.py runserver`
- It should work at this point
- If there is a problem with the db remove everything in the folder `lfc-api/LookingForConcerts/lfc_backend/migrations`
- Create an empty python file named `__init__.py` in the migrations folder
- Run `python manage.py makemigrations && pyhton manage.py migrate`
- Again run the server `python manage.py runserver`

# How to test
- Go into the directory `lfc-api/LookingForConcerts` in our repository
- Run the command `python manage.py test lfc_backend/`

# Important points
- If you would like to deploy the django app on a different host, you should change the HOST variable in django settings file and all the host variables in the front end files.
- Notice that if you change the host, Spotify connect would not work since the redirect uri should be whitelisted.
