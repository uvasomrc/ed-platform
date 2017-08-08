## Development

This is (in part) a Python3 application that depends on the Anaconda platform.

### Dependencies
* [Anaconda](https://www.continuum.io/downloads) Download for your
  operating system, and be sure to select Python3.  Excellent
    documentation on using Anaconda in a virtual envionrment in this
      [eResearch Cookbook](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

* [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
  You will need ElasticSearch, running locally on your computer.

### Setup
```BASH
$ git clone git@github.com:uvasomrc/ed-platform.git
$ conda env create -n ed-platform
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
the command above.  In the event you need to install a new **Conda** package,
be sure to tell it to install in the current environment, like so:
```BASH
$ conda install -n ed-platform [package-name]
```
For Pip packages this is handled automatically, just do:
```BASH
$ pip install [package-name]
```

NOTE: When you install new packages, be sure to update the environment.yml
file manually with the correct library and version, or regenerate one with
```BASH
$ conda env export > environment.yml
```
That way the next person can just update and they are good to go.

#### Updating your packages
When you do a pull request, it's good practice to try and
import any new libraries others may have added to the project.
You can do this with:
```BASH
$ conda env update
```

#### Dealing with CORS
Cross-origin requests may be an issue when getting the front end
and back end talking to each other.  For this reason I recommned using
Chrome and [this plugin](https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi) that will allow you to disable and enable
CORS as needed.


### PyCharm
If you are using pycharm, be sure to set your interpreter to point to
virtual environment you created.  For this this was located in the
directory where I installed Anaconda (/home/dan/bin/Anaconda)  From there
it was located in /env/ed-platform/bin/python

Once properly configured, PyCharm will be fully aware of all the libraries
in the environment.yml file mentioned above.


