
This is (in part) a Python3 Flask application that depends on the
Anaconda platform for managing dependencies.


# Development

There is a bash script in .env that will automatically activate the
ed-platform environment, and set some evironment variables.  This
script will run automatically when you cd into the directory if you
have installed [autoenv](https://github.com/kennethreitz/autoenv)
These instructions will work for Mac and Linux systems:
```BASH
$ deactivate
$ pip install autoenv==1.0.0
$ echo "source `which activate.sh`" >> ~/.bashrc
$ source ~/.bashrc
```
Then cd out and back into the backend directory, and your environment
should be properly configured to run in Development.

*NOTE*: There is a [plug in for Pycharm](https://plugins.jetbrains.com/plugin/7861-env-file)
 that will allow you to use this same environment file in your run configuration.

## Dependencies
* [Anaconda](https://www.continuum.io/downloads) Download for your
  operating system, and be sure to select Python3.  Excellent
    documentation on using Anaconda in a virtual envionrment in this
      [eResearch Cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

* [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
  You will need ElasticSearch, running locally on your computer.

* [Postgres] (https://www.postgresql.org/) Version 9.7 or later.

## Python Setup
```BASH
$ git clone git@github.com:uvasomrc/ed-platform.git
$ cd ed-platform/backend
$ conda env create -f environment.yml
$ source activate ed-platform
```

Going forward you will need to activate this environment each time
you start a new terminal session.

You can do so with:
```BASH
$ source activate ed-platform
```

#### Adding New Packages
NOTE:  All packages you need for this project are already installed using
the command above.  In the event you need to install a new package,
find it using conda search, then add it in by updating your environment.
Following this process will assure that others also get the new library
when they check out the code.
```BASH
$ conda search sqlalchemy
Fetching package metadata .........
sqlalchemy
                             .
                             .
                             .
                             1.1.10                   py27_0  defaults
                             1.1.10                   py35_0  defaults
                             1.1.10                   py36_0  defaults
                             1.1.11                   py27_0  defaults
                             1.1.11                   py35_0  defaults
                             1.1.11                   py36_0  defaults
```
Then Update the evironment.yml file, with the correct syntax.
```YAML
name: ed-platform
channels:
- defaults
dependencies:
- flask=0.12.2=py36_0
.
.
.
- sqlalchemy=1.1.11=py36_0
```

#### Updating your packages
When you do a pull request, it's good practice to try and
import any new libraries others may have added to the project.
You can do this with:
```BASH
$ conda env update
```

### Working with PyCharm
If you are using pycharm, be sure to set your interpreter to point to
virtual environment you created.  For me personally, this was located in the
directory where I installed Anaconda (/home/dan/bin/Anaconda)  From there
it was located in /env/ed-platform/bin/python

Once properly configured, PyCharm will be fully aware of all the libraries
in the environment.yml file mentioned above.

## Database Configuration
We are using Postgres, version 9.5.7 or later.

### Creating a Database
```BASH
$ sudo su postgres
$ psql
postgres=# create database ed_platform
postgres=# \q
$ exit
```

### Database Definition
```BASH
python manage.py db init
```

### Updating the Database
You will need to update your database each time you return to do a
pull to make sure all the migrations are run.  Use this:
```BASH
python manage.py db update
```

