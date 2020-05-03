import os
import json

with open('/etc/config.json') as config_file:  # make config.json file in Linux system with environment variables for secret key and database URI
	config = json.load(config_file)

class Config:
    SECRET_KEY = 'd168651a2aa242e14428a991c42164ef'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:your_password_here@localhost/groundwater'
