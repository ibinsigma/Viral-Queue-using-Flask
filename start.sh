#!/bin/bash
cd Authen/auth 
export FLASK_ENV=development
export FLASK_APP=project
echo "STARTING SERVER AFTER 1 minute"
echo "Kindly Read the script for details"
sleep 1m
flask run
# If you are running for the first time , then create the database
# cd into /auth , open python shell and type the following commands
# from project import db, create_app
# db.create_all(app=create_app())




# ----

#	Process is not being killed since the server is set up locally .
#	After deployment , a '/shutdown' route can be created to stop the server after 1 month
