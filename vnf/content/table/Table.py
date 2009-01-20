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


class Table(object):

    def __init__(self, model, data, view):
        self.model = model
        self.data = data
        self.view = view
        return

    pass # end of Table


def test():

    from model.Model import Model as ModelBase
    class Model(ModelBase):
        
        a = ModelBase.Measure(name='a', type='str')
        b = ModelBase.Measure(name='b', type='integer')

    class D:
        def __init__(self, a, b):
            self.a = a
            self.b = b
            return
    data = [D('hello', 345)]

    from view.View import View as ViewBase
    class View(ViewBase):
        
        columns = [
            ViewBase.Column(measure='a'),
            ViewBase.Column(measure='b'),
            ]

    table = Table(Model, data, View)
    return


def main():
    test()
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
