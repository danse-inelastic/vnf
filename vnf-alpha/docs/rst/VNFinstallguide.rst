VNF Install Guide
=================

This walkthrough assumes a fresh Ubuntu or Fedora install.  However, any part of the guide can be theoretically apply to any unix-based system.  This guide assumes no background whatsoever in unix-based systems.

CACR
----

To aquire a CACR account first generate a `SSH key <http://www.cacr.caltech.edu/main/?page_id=85>`_.  Then head over to the `CACR Registration Site <http://www.cacr.caltech.edu/main/?page_id=477>`_ . VNF can still be installed with read-only access.

Configuring Your Environment
----------------------------

There are several packages that need to be installed prior to actually installing VNF.  

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

For Ubuntu, open a terminal and type 'sudo apt-get install' and each of the package names in the following list. 

For Fedora, log in to root and type 'yum install' and each of these package names.

- subversion
- postgresql-8.3
- postgresql postgresql-server
- pgadmin3 (Optional)
- wxPython
- numpy
- matplotlib
- hdf5

Test wxPython, numpy, and matplotlib by making sure there are no errors when you type, in terminal::

	python
	>>> import wx
	>>> import numpy
	>>> import matplotlib

Downgrading to Python 2.5
~~~~~~~~~~~~~~~~~~~~~~~~~

Note: Pyre and VNF have been known to work with Python 2.6 on Fedora 11, so try continuing with installation without downgrading from Python 2.6 first. 

For Ubuntu, to install Python 2.5 onto your system, open terminal and type in this code::

	sudo apt-get install python2.5

Edit the /usr/share/python/debian_defaults, changing the default version arg to python2.5.

Open terminal and type this code in::

	sudo mv /usr/bin/python /usr/bin/python2.5
	sudo ln -s /usr/bin/python2.6 /usr/bin/python
 

Make.mm
~~~~~~~~

Throughout these instructions, it will be assumed that everything is installed in /home/username, for example's sake. It is highly recommended to not install VNF as root unless a step in the instructions says to, to prevent problems with file permissions.

Follow the instructions :ref:`here <make-mm>`.

As mentioned in the detailed instructions for Make.mm, a shortcut is to download this :download:`bash <bash_tools.linux>` file and then move it to your home directory (/home/username).  Make sure it is named bash_tools.linux.

In terminal, navigate to your home directory and execute this code::

	. ./bash_tools.linux

You will need to execute this command every time you start a terminal (a shortcut might be to add it to your .bashrc).

Checking Python and Make.mm Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	
If you downgraded to Python2.5, try the following. If you did not downgrade, you can skip this step.
In terminal, execute this code::

	env
	
After you execute env, you should see a mass of text that describe a variety of enviromental variables.  The variables that you want to look for to check the validity of all you have installed so far are::

	PYTHON_VERSION=2.5
	PYTHONSTARTUP=(whatever your root directory is)/.python
	PYTHON_LIBDIR=/usr/lib/python2.5
	

Pyre Install
-------------

In terminal, navigate to root and type this code in::

	svn co svn+ssh://svn@danse.us/pyre/branches/patches-from-jiao
	cd patches-from-jiao/
	mm

Check to make sure Pyre and Make.mm are properly installed by typing in terminal::

	cd
	app.py

which should produce the message: "creating application 'Simple' in 'simple.py'".


Histogram Install
-----------------

Follow the instructions `here <http://dev.danse.us/trac/histogram/wiki/Install-0.1_from_svn>`_ to install the histogram package after you finish installing Pyre. Then, copy the necessary files from tmp to your pyre directory (so the main.cgi supplied below will work) by typing in terminal::

	cd $EXPORT_ROOT/packages
	mkdir histogram
	cd histogram
	cp -r /tmp/histogram-0.1/modules/* .

Where $EXPORT_ROOT is, for example, /home/username/dv/tools/pythia-0.8

Downloading VNF
---------------

In terminal, go to where you would like to install VNF and type::

	svn co svn://danse.us/VNET/vnf/releases/alpha
	cd alpha
	mm

Configuring the Database
------------------------

For Ubuntu, open a terminal and type::

	sudo su postgres -c psql template1
	createdb vnf

In Fedora, logged in as root, type in a terminal::

        service postgresql start
	su -- postgres
	psql template1
	CREATE USER username WITH PASSWORD 'password';
	\q
	createdb vnf

Where username is one that matches the apache httpd.conf file (in Apache Configuration, below) and is consistent with the username used throughout this installation. 

Remote DB Servers
-----------------

If you installed PostgreSQL on the machine where you installed VNF, you can skip this step. If not, modify $VNF_EXPORT/config/clerk.pml (where $VNF_EXPORT is where VNF is installed. For example, /home/username/alpha). The default clerk.pml is::

	<inventory>

	  <component name='clerk'>
	     <property name='db'>vnf</property>
	     <property name='dbwrapper'>psycopg2</property>
	  </component>

	</inventory>

where the property "db" tells the vnf applications where to connect to database. The default value "vnf" means that a unix domain socket connection to the local PostgreSQL db server is used, and the database name is "vnf". To connect to a remote db server, the value of "db" should be something like::

	username:password@hostname:port:database

or, to take a specific case::

	vnf:1234567@db.server:5432:vnf 

psycopg2 Install
-----------------

Download the tarball from a `direct link <http://www.initd.org/pub/software/psycopg/psycopg2-2.0.11.tar.gz>`_, then extract the files inside the tarball into an easily accessible place (preferably root).  Run the setup files.

If there are error messages, it may be necessary to download header files for postgresql.

Apache Server Install and Configuration
-----------------------------------------

For Fedora, type in terminal, logged in as root::

	yum install httpd

Alternatively, download the Apache install files `here <http://www.gtlib.gatech.edu/pub/apache/httpd/httpd-2.2.11.tar.gz>`_ and install Apache.

Start up your Apache server by typing in terminal (as root)::

	apachectl start

Apache Configuration
~~~~~~~~~~~~~~~~~~~~~

Next, enable CGI.  For Ubuntu, through terminal, navigate to the directory `~/etc/apache2/sites-enabled/000-default` and enter this code::

	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
	<Directory "/usr/lib/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

For Fedora, open the file /etc/httpd/conf/httpd.conf and enter this::

	ScriptAlias /cgi-bin/ /var/www/cgi-bin/
	<Directory "/var/www/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

Also, you may need to find where it says::

	User apache
	Group apache 

and change apache to your username (which matches your database username). 

If using Fedora, disable SELinux (System > Administration > SELinux Management) to allow apache to access user directories. You may have to reboot your machine to make this take effect.  

After making changes to httpd.conf, restart the server by logging in to root and type::

	apachectl restart

Then, make a directory that serves CGI.  For Ubuntu, in terminal::

	sudo mkdir /usr/lib/cgi-bin/vnf
	sudo cd /usr/lib/cgi-bin/vnf

For Fedora, in terminal::

	mkdir /var/www/cgi-bin/vnf
        cd /var/www/cgi-bin/vnf

Make a simple CGI (main.cgi) that sets up enviromental variables and also calls the VNF application. Assuming vnf was downloaded in /home/username/alpha and Pyre was installed following the Make.mm instructions in /home/username/dv/tools/pythia-0.8, main.cgi should contain::

	#!/usr/bin/env bash

        VNFINSTALL=/home/username/alpha
        PYREINSTALL=/home/username/dv/tools/pythia-0.8
	export PATH=$VNFINSTALL/bin:$PATH
	export PYTHONPATH=$PYREINSTALL/packages/histogram:$PYTHONPATH
	export PYTHONPATH=$PYREINSTALL/packages:$PYTHONPATH
	export LD_LIBRARY_PATH=$PYREINSTALL/lib:$LD_LIBRARY_PATH
	export PYRE_DIR=$PYREINSTALL/packages:$PYRE_DIR
	cd $VNFINSTALL/cgi && python main.py $@

Adjust the above code as needed (i.e. replace username with your username) and make sure main.cgi is executable::

        chmod +x main.cgi

HTML content needs to be made available by creating a symbolic link. In the below instructions, $VNF_EXPORT refers to where you installed VNF (for example, /home/username/alpha).

For Ubuntu, type in terminal::

	sudo cd /var/www
 	sudo ln -s $VNF_EXPORT/html vnf

For Fedora, in terminal as root::

	cd /var/www/html
	ln -s $VNF_EXPORT/html vnf

To configure the vnf web application, you will need to put these new paths in $VNF_EXPORT/config/main.pml. Edit main.pml to contain::

	<inventory>
	
	  <component name='main'>
	    <property name='home'>http://localhost/vnf/</property>
	    <property name='cgi-home'>http://localhost/cgi-bin/vnf/main.cgi</property>
	    <property name='imagepath'>/vnf/images</property>
	    <property name='javascriptpath'>/vnf/javascripts</property>
	  </component>
	
	</inventory>

Start Daemons
-------------

With the db properly functioning, we can initialize three vnf services (a journal daemon, a unique identifier generator daemon, and an authentication daemon) by executing the shell script::

	 cd $VNF_EXPORT/bin
	 ./startservices.sh

or::

        cd $VNF_EXPORT/bin
        ./journald.py
        ./idd.py
        ./ipad.py

You will also want to initialize the vnf database with some tables by executing the python script within $VNF_EXPORT/bin::

 	./initdb.py

If this fails, it usually means your database connection was not configured correctly. Go reconfigure first.

Test Your VNF Installation
--------------------------

Open your browser and go to http://localhost/cgi-bin/vnf/main.cgi. You should see the VNF login page. 

If that does not work, try http://localhost/cgi-bin/vnf/main.cgi?actor=login instead. See Troubleshooting, below, if there are problems.

Configuring Your Computational Cluster
--------------------------------------

For each cluster or machine on which VNF launches jobs, a scheduler needs to be installed. VNF has been tested with torque. Information on downloading and installing torque is `here <http://www.clusterresources.com/wiki/doku.php?id=torque:appendix:l_torque_quickstart_guide>`_. Then install either the built-in scheduler in torque, pbs_scheduler, or `Maui <http://www.clusterresources.com/pages/products/maui-cluster-scheduler.php>`_.

For each cluster/machine where vnf jobs will be launched, add an entry to the "servers" table in the "vnf" database by using, for example, pgadmin3. The record is used to describe the computation server. For example, the columns id, address, username, workdir, and scheduler might be: 

    * id: octopod
    * address: octopod.danse.us
    * username: vnf
    * workdir: /home/vnf/vnfworkdir
    * scheduler: torque 

To access the server, an authentication method needs to be available. Currently ssh is used. To set up ssh access:

   1. create private/public key pair
   2. add the public key to the remote computational server's .ssh/authorized_keys
   3. edit $VNF_EXPORT/config/ssher.pml to point to these keys 

Troubleshooting
---------------

Error log locations:

- For apache: /var/log/httpd
- For vnf: $VNF_EXPORT/log

You could also try running VNF out of /home/username/dv/tools/pythia-0.8/vnf instead of /home/username/alpha. This directory should already exist if you installed Make.mm and Pyre.

And main.cgi should be changed to the following (with username changed to your username, etc.)::

	#!/usr/bin/env bash

        VNFINSTALL=/home/username/dv
        EXPORT_ROOT=$VNFINSTALL/tools/pythia-0.8
        export PATH=$EXPORT_ROOT/bin:$PATH
        export PYTHONPATH=$EXPORT_ROOT/packages/histogram:$PYTHONPATH
        export PYTHONPATH=$EXPORT_ROOT/packages:$PYTHONPATH
        export LD_LIBRARY_PATH=$EXPORT_ROOT/lib:$LD_LIBRARY_PATH
        export PYRE_DIR=$EXPORT_ROOT/packages:$PYRE_DIR
        cd $EXPORT_ROOT/vnf/cgi && python main.py $@

and $VNF_EXPORT in the instructions above would refer to /home/username/dv/tools/pythia-0.8/vnf, for example.

