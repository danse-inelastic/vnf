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


buildbot
""""""""
A buildbot system will run tests automatically. Currently tests in the
following test directories are included in the buildbot system:

* tests/vnfb
* tests/selenium


