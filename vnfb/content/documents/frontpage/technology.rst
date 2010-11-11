.. _technology:

Technology
==========

Infrastructure
--------------
* `python <http://www.python.org>`_: The VNF web application is implemented by using python
* `pyre <http://docs.danse.us/pyre/sphinx/>`_, a large-scale, high-performance scientific-computing framework, is the backbone of the VNF.


User interface
--------------

* `luban <http://luban.danse.us>`_. The user interface of the VNF is built by using luban,
  a generic user interface language. The web presentation of the VNF
  is rendered by luban into html,
  `javascript <http://en.wikipedia.org/wiki/JavaScript>`_, 
  `ajax  <http://en.wikipedia.org/wiki/Ajax_(programming)>`_,
  and `json <http://www.json.org>`_.
* The 3D viewer is implemented using `plugin-o3d <http://code.google.com/apis/o3d/>`_ and will be migrated to `webgl-o3d <http://code.google.com/p/o3d/>`_.


Scientific computing
--------------------
Various scientific computing packages are used to calculate
material properties and simulate neutron scattering experiments.


Monte Carlo simulation of neutron scattering
""""""""""""""""""""""""""""""""""""""""""""

* MCViNE (http://docs.danse.us/MCViNE) is the Monte Carlo simulation framework
  that suppors the simulations of virtual neutron experiments in VNF.
* McStas (http://www.mcstas.org), a neutron ray-tracing simulation package,
  provides many mc neutron components used by MCViNE.


Molecular dynamics
""""""""""""""""""

Ab initio quantume chemistry simulations
""""""""""""""""""""""""""""""""""""""""



