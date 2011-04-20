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
        html_base = self.inventory.html_base
        controller_url = self.inventory.controller_url
        
        t = open('index.html.template').read()
        c = t.replace('xxxBASExxx', html_base)
        c = t.replace('xxxCONTROLLERxxx', controller_url)
        open('index.html', 'w').write(c)
        
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']



def main():
    app = App()
    app.run()
    return


if __name__ == '__main__': main()
