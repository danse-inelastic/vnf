# -*- python -*-

from pyre.applications.Script import Script as base
class App(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        controller_url = pyre.inventory.str('controller-url')
        html_base = pyre.inventory.str('html-base')

    
    def __init__(self, name='web-weaver'):
        super(App, self).__init__(name)
        return
    
    
    def main(self):
        self._createFromTemplate('index.html')
        self._createFromTemplate('atomicstructure.html')
        self._createFromTemplate('phonons.html')
        self._createFromTemplate('arcs.html')
        return


    def _createFromTemplate(self, filename):
        html_base = self.inventory.html_base
        controller_url = self.inventory.controller_url

        template = '%s.template' % filename
        t = open(template).read()
        c = t % locals()
        open(filename, 'w').write(c)
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']



def main():
    app = App()
    app.run()
    return


if __name__ == '__main__': main()
