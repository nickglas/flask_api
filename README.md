#### SHOOTSOFT FLASK PROJECT BUILD ON RESTX BOILER-PLATE WITH JWT(PYTHON 3.10)

### Requirements
In order for this application to work you will need to have `pip`, `python 3.10` and a `virtual envirioment` installed.

[Python 3.10](https://www.python.org/downloads/release/python-3100/)<br />
[virtual envirioment (venv)](https://docs.python.org/3/library/venv.html)


### Automatic installer
The windows build uses `venv` and can be activated manually from the project root by typing `venv\Scripts\activate.bat` into a cmd prompt or run start.py

    To run application: run the start.py file or the start.bat(WINDOWS ONLY)

The flask application will start with no database. In order to create a new database you will need to follow the options inside the menu. Menu item 5 will drop the database, create a new migration and create a new database.

### Manual installer
If the automatic installer is not working, then follow these steps to manually install the required packages. Please execute these commands in order.

Initialize new virtual envirionment
```shell script
python -m virtualenv venv
```
A new virtual envirionment will be created and a folder called 'venv' will be created in the root folder <br /><br />

Activate the new virtual envirionment
```shell script
venv\Scripts\activate.bat
```
The new virtual envirionment will be activated<br /><br />

Installing required packages
```shell script
pip install -r requirements.txt
```
Packages will be installed into the new virtual envirionment<br /><br />

### Starting the app
In order to start the application, either start it with the start.bat file or run the start.py with the following command.
```shell script
python start.py
```

### Viewing the app ###
    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman / Insomnia ####
    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.


### Based on : Full description and guide (beware this guide targets an older python version!) ###
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

