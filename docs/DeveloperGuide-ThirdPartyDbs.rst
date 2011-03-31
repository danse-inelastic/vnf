.. _vnfdeveloperguidedom:

Third party databases
======================

VNF uses a number of third-party databases such as COD, NIST experimental neutron repository, etc.  Here we explain how to set these up.


Crystallography Open Database (COD)
----------------------------------------
Prerequisites:

* mysql
.. * phpmysqladmin

To set up COD one must use an existing mirror or set up a mirror of COD.  To set up a mirror on, say, vnf-dev.caltech.edu: 

#. First checkout the database

   svn checkout svn://www.crystallography.net/cod

#. Create a database named 'cod' (i.e. mysql> create database employees;). Then navigate to cod/mysql/ and execute cod-load-mysql-dump.sh.  This should populate the database with the current dataset.  

#. Modify the db connection properties, usually in /etc/mysql/my.cnf, to

   bind-address		= vnf-dev.caltech.edu

#. Create user vnf with password 'somepassword':

   mysql> CREATE USER 'vnf'@'%' IDENTIFIED BY 'somepassword';
	
   mysql> GRANT ALL PRIVILEGES ON *.* TO 'vnf'@'%' WITH GRANT OPTION;

#. You should be able to connect to your host:

   mysql --user=vnf --database=cod --host=vnf-dev.caltech.edu -p


NIST experimental neutron repository
----------------------------------------



