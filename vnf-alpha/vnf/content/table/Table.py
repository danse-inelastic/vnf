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
        self.contents = []
        return

    def identify(self, visitor): return visitor.onTable(self)

    pass # end of Table



def example():
    from model.Model import Model
    class model(Model):
        
        title = Model.Measure(name='title', type='text')
        date = Model.Measure(name='date', type='date')

    class D:
        def __init__(self, title, date):
            self.title = title
            self.date = date
            return
    data = [
        D( 'abc', '06/06/2006' ),
        D( 'hi', '05/05/2005' ),
        ]

    from view.View import View as View
    class view(View):
        
        columns = [
            View.Column(id='col1',label='Title', measure='title'),
            View.Column(id='col2',label='Date', measure='date',
                        valid_range=[ '01/01/1977', '01/01/2008' ])
            ]

        editable = False

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
