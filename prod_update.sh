#!/bin/bash

# Run the basic operations to update a production setup after a code change.
# This script should be executed by a post_recieve git hook after completing
# a checkout.
# --------------------------------------------------------------------------

# Move the configuration file into place.
mkdir -p ./backend/instance
cp /home/ubuntu/edp_config.py ./backend/instance/config.py

if [ "$1" == "prod" ]; then
    echo "Building for production."
elif [ "$1" == "staging" ]; then
    echo "Building for staging."
else
    echo "Please specify environment (prod/staging)"
    exit
fi

export ENV=$1
# Eat at Joes
# Update the database
source /home/ubuntu/anaconda3/bin/activate edp
export HOME_DIR=`pwd`
echo "Running from ${HOME_DIR}"
# Continue to update conda in case I can get that working ...
eval 'cd ${HOME_DIR}/backend && conda env update'
# But also install via pip3, which is what the production server is using now.
eval 'pip3 install flask sqlalchemy psycopg2 flask-migrate flask-script flask-cors flask-marshmallow flask-compress marshmallow-sqlalchemy flask-sso pyjwt flask-httpauth flask_mail elasticsearch_dsl flask-uploads python-magic requests-toolbelt icalendar markdown2'
if [ "$ENV" == "staging" ]; then 
   eval 'python ${HOME_DIR}/backend/manage.py cleardb'
   eval 'python ${HOME_DIR}/backend/manage.py clearindex'
fi
eval 'cd ${HOME_DIR}/backend && python ${HOME_DIR}/backend/manage.py db upgrade'
if [ "$ENV" == "staging" ]; then 
   eval 'cd ${HOME_DIR}/backend && python ${HOME_DIR}/backend/manage.py initdb'
fi
eval 'cd ${HOME_DIR}/backend && python ${HOME_DIR}/backend/manage.py initindex'
# Rebuild the front end.
eval 'cd ${HOME_DIR}/frontend && npm install'
eval 'cd ${HOME_DIR}/frontend && ng build -c ${ENV}'


# Reload apache
echo "Reloading Apache"
sudo service apache2 reload

