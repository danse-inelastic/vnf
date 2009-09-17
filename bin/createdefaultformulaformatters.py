#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class CreateDefaultFormulaForMatters(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        pass # end of Inventory
        

    def main(self):
        db = self.clerk.db

        from vnf.dom import mattertables
        tables = mattertables()

        from vnf.dom.MatterBase import buildFormula
        
        for table in tables:
            records = db.fetchall(table)
            for r in records:
                if not r.chemical_formula:
                    r.chemical_formula = buildFormula(r)
                    db.updateRecord(r)
            continue
        
        return


    def _configure(self):
        base._configure(self)

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)
        return




def main():

    class App(CreateDefaultFormulaForMatters):


        def _getPrivateDepositoryLocations(self):
            return ['../config', '/tmp/luban-services']


    app = App(name='createdefaultformulaformatters')
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
