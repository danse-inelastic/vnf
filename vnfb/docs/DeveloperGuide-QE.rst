.. _vnf_developer_guide_qe

Architecture of Quantum Espresso Simulation
===========================================

Introduction
------------

In the beginning there was a command line, and the command line was dark and
the green ASCII characters were with it. Through it all things were made and
without it nothing was made that has been made. :)

{About Quantum Espresso package architecture }

Architecture Overview
---------------------

Simulation Chains
-----------------

Simulation Workflow
-------------------

Database Schema
---------------

Here is the database schema for Quantum Espresso simulation. The main table
``qesimulations`` has many-to-many relationship with ``qetasks`` through
``qesimulationtasks``

.. figure:: images/qe-dev/dbschema.png
   :width: 720px

   *Fig. Database schema for Quantum Espresso simulation*


Inputs
------

Input Generators
^^^^^^^^^^^^^^^^

Input Fiters
^^^^^^^^^^^^

Jobs
----

Job Submission
^^^^^^^^^^^^^^

Job Status
^^^^^^^^^^
    
Results
-------

Results Retrieval
^^^^^^^^^^^^^^^^^

Results Export
^^^^^^^^^^^^^^

Simulation Optimization
-----------------------

Convergence Tasks
-----------------

Applications
------------



