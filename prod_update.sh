File Edit Options Buffers Tools Sh-Script Help
#!/bin/bash

# Run the basic operations to update a production setup after a code change.
# This script should be executed by a post_recieve git hook after completing
# a checkout.
# --------------------------------------------------------------------------

# Move the configuration file into place.
mkdir -p ./backend/instance
cp /home/ubuntu/edp_config.py ./backend/instance/config.py

# Update the database
source /home/ubuntu/anaconda3/bin/activate edp
export HOME_DIR=`pwd`
echo "Running from ${HOME_DIR}"
eval 'python ${HOME_DIR}/backend/manage.py clear_data'
eval 'cd ${HOME_DIR}/backend && python ${HOME_DIR}/backend/manage.py db upgrade'
eval 'cd ${HOME_DIR}/backend && python ${HOME_DIR}/backend/manage.py load_data'
# Rebuild the front end.
eval 'cd ${HOME_DIR}/frontend && npm install'
eval 'cd ${HOME_DIR}/frontend && ng build -prod'

# Reload apache
echo "Reloading Apache"
sudo service apache2 reload

