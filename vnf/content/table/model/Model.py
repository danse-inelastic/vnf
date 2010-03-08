# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class MeasureCollector (type):


    def __init__(cls, name, bases, dict):
        import sys
        vinfo = sys.version_info
        if vinfo[0]< 2 or vinfo[0]==2 and  vinfo[1] < 6:
            type.__init__(name, bases, dict)
        else:
            type.__init__(cls, name, bases, dict)

        measureRegistry = {}

        # register inherited traits
        bases = list(bases)
        bases.reverse()
        for base in bases:
            try:
                measureRegistry.update(base._measureRegistry)
            except AttributeError:
                pass

        # scan the class record for traits
        for name, item in cls.__dict__.iteritems():

            # disregard entries that do not derive from Measure
            if not isinstance(item, cls.Measure):
                continue

            # register it
            measureRegistry[item.name] = item
            
        # install the registries into the class record
        cls._measureRegistry = measureRegistry
        return



class Model(object):

    name = None

    from Measure import Measure

    def measures(cls):
        return cls._measureRegistry.iteritems()
    measure = classmethod(measures)

    def getMeasure(cls, name):
        return cls._measureRegistry[name]
    getMeasure = classmethod(getMeasure)

    __metaclass__ = MeasureCollector
    pass


def test():
    class MyModel(Model):
        a = Model.Measure(name='a', type='time')
        b = Model.Measure(name='b', type='str')
    return


# version
__id__ = "$Id$"

# End of file 
