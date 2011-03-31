.. _vnfdeveloperguidetests:

Tests
=====

All tests should be under directory "tests" in the vnfb source tree.

All selenium tests should be under directory "tests/selenium" in the
vnfb source tree.

More details of the "tests" directory structure:

* vnfb: tests of vnfb python package
* selenium: selenium tests of UI
* content/components: tests of components
* eclipse: tests based on eclipse


Automatic test system
"""""""""""""""""""""
Testing software products for quality assurance is essental for software
projects. VNF is a complex project involving multiple software packages,
and its automatic test system helps reduce tedious work of running 
repetitive tests.

We deployed a buildbot system that will run tests automatically whenever 
there are new check-ins to VNF code base.

The following packages are included in the buildbot system:

* luban
* histogram
* bvk
* vnf

For vnf package, currently the
following test directories are included in the buildbot system:

* tests/vnfb
* tests/content
* tests/selenium

VNF computing nodes makes heavy use of the MCViNE (http://docs.danse.us/MCViNE).
MCViNE is itself a fairly complex package and has its own
buildbot system: http://bagua.cacr.caltech.edu:50082


