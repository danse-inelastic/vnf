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



def example():
    from model.Model import Model
    class model(Model):
        
        a = Model.Measure(name='a', type='str')
        b = Model.Measure(name='b', type='integer')

    class D:
        def __init__(self, a, b):
            self.a = a
            self.b = b
            return
    data = [D('hello', 345)]

    from view.View import View as View
    class view(View):
        
        columns = [
            View.Column(measure='a'),
            View.Column(measure='b'),
            ]

    table = Table(model, data, view)
    return table


def test():
    table = example()
    return


def main():
    test()
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
