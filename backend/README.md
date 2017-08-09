
This is (in part) a Python3 Flask application that depends on the
Anaconda platform for managing dependencies.

# Dependencies
* [Anaconda](https://www.continuum.io/downloads) Download for your
  operating system, and be sure to select Python3.  Excellent
    documentation on using Anaconda in a virtual envionrment in this
      [eResearch Cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

* [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
  You will need ElasticSearch, running locally on your computer.

* [Postgres] (https://www.postgresql.org/) Version 9.7 or later.

# Python Setup
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

# Database Configuration
We are using Postgres, version 9.5.7 or later.

### Creating a Database
```BASH
$ sudo su postgres
$ psql
postgres=# create database ed_platform
```



