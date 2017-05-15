<img 
name="cover-pic"
src="https://drive.google.com/uc?export=view&id=0BwxjlJsvjKMLSnVmOGRJOVVlZFk"
height=200>

# Concert API
Concert API is the API for a small part of our Concert project. You can perfom CRUD operations on Concerts and Users.

## Setup
Assuming that you have pip, install django as follows:
```
pip install django
pip install djangorestframework
pip install pygments
```
After these installations 

Create a folder to copy the branch.

Clone the repository: 
```
git clone https://github.com/bounswe/bounswe2017group2.git ~/Desktop/swe2017
```
Move into the folder of the api: 
```
cd ~/Desktop/swe2017/API\ Test\ App/ConcertAPI
```
Yes we have 2 concerts API folders consecutively.

Activate the environment: 
```
source env/bin/activate
```
Run the server:
```python manage.py runserver```

Or, to run the tests:
```python manage.py test```

## Endpoints
### Concert Endpoints (/concert/)

* **Get All Concerts [GET]**

  You can get all concert by sending a GET request. 
  
  Parameters: None
  
  Example Request:
  
  `http http://127.0.0.1:8000/concert/`
  
  Example Response:
  
  Response code: 200, OK
  
  ```JSON
  [
     {
        "id": 1, 
        "artist": "Duman", 
        "location": "BogaziciUniTasoda", 
        "date": "2017-05-20", 
        "minprice": 0, 
        "maxprice": 0
      },
      {
         "id": 2, 
         "artist": "Bulent Ortacgil", 
         "location": "BogaziciUniTasoda", 
         "date": "2017-05-21", 
         "minprice": 0, 
         "maxprice": 0
       }
    ]
  ```
   
* **Get A Specific Concert [GET]**

  You can get a specific concert by sending a GET request with that concert's id. 
  
  Parameters: 
  * Concert ID
  
  Example Request:
  
  `http http://127.0.0.1:8000/concert/1/`
  
  Example Response:
  
  Response code: 200, OK
  
  ```JSON
   {
      "id": 1, 
      "artist": "Duman", 
      "location": "BogaziciUniTasoda", 
      "date": "2017-05-20", 
      "minprice": 0, 
      "maxprice": 0
    }
  ```
* **Create New Concert [POST]**

  You can create a new concert by giving appropriate parameters.
  
  Parameters: 
  * Artist (required)
  * Location (required)
  * Date (required)
  * Min-Price
  * Max-Price
  
  Example Request:
  
  `http --json POST http://127.0.0.1:8000/concert/ artist="John Mayer" location="LA" date="2017-08-08" minprice=200 maxprice=400`
  
  Example Response:
  
  Response code: 201, CREATED
  
  ```JSON
   {
      "id": 1, 
      "artist": "John Mayer", 
      "location": "LA", 
      "date": "2017-08-08", 
      "minprice": 200, 
      "maxprice": 400
    }
  ```  

* **Update A Concert [PUT]**

  You can update a concert by giving the appropriate parameters.
  
  Parameters: 
  * Concert ID (required)
  * Artist (required)
  * Location (required)
  * Date (required)
  * Min-Price
  * Max-Price
  
   Example Request:
   
  `http --json PUT http://127.0.0.1:8000/concert/1/ artist="Sebnem Ferah", location = "BogaziciUniTasoda", date = "2017-06-20", minprice = 50, maxprice = 200`
  
  Example Response:
  
  Response code: 200, OK
  
  ```JSON
   {
      "id": 1, 
      "artist": "Sebnem Ferah", 
      "location": "BogaziciUniTasoda", 
      "date": "2017-06-20", 
      "minprice": 50, 
      "maxprice": 200
    }
  ```  
  
* **Delete A Concert [DELETE]**

### User Endpoints (/user/)

* **Get All Users [GET]**
* **Get A Specific User [GET]**
* **Create New User [POST]**
* **Update A User [PUT]**
You can update a user by giving the appropriate parameters.
  
  Parameters: 
  * Name
  * e-mail
  * Password
  * Age
  
  Example Request:
  
  `http --json PUT http://127.0.0.1:8000/user/1/ name="Sebnem Ferah", email = "sferah@gmail.com", password = "ferahla", age = 44`
  
  Example Response
  
  Response code: 200, OK
  
  ```JSON
   {
      "id": 1, 
      "name": "Sebnem Ferah", 
      "email": "sferah@gmail.com", 
      "password": "ferahla", 
      "age": 44
    }

* **Delete A User [DELETE]**
