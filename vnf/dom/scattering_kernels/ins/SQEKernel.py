# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import Phonons, AbstractScatteringKernel as base

class SQEKernel(base):

    sqe = None

    Qmin = 0.
    Qmax = 10.

    Emin = -50.
    Emax = 50.
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = [
            'sqe',
            'Emin', 'Emax',
            'Qmin', 'Qmax',
            ]
        #
        def _createfield_for_sqe(obj):
            # this is a method of mold.
            self = drawer.mold

            # imports
            import luban.content as lc
            from luban.content import load, select
            from luban.content.FormSelectorField import FormSelectorField
            
            # utils
            orm = self.orm

            # data 
            record = self.orm(obj)
            referred_record = record.sqe and record.sqe.id \
                              and record.sqe.dereference(self.orm.db)

            # widget
            doc = lc.document(Class='container', id='sqe-selector-container')
            sp = doc.splitter()
            left = sp.section(); right = sp.section()
            #
            selector = FormSelectorField(label='Sqe:', name='sqe')
            left.add(selector)
            #
            plotcontainer = right.document(Class='container')
            #
            loadplot = lambda uid: load(
                actor='orm/sqe', routine='createGraphicalView',
                uid=uid)

            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
                plotcontainer.oncreate = select(element=plotcontainer).append(
                    loadplot(value))
            else:
                value=None

            # choices
            #  get matter
            matter = orm.db.dereference(record.matter)
            matterid = matter.id
            #  dynamically load choices
            entries = load(
                actor='orm/atomicstructures',
                routine='getSelectorEntriesForSqe',
                id = matterid,
                include_none_entry = 1,
                )
            selector.oncreate = select(element=selector).setAttr(entries=entries, value=value)
            selector.onchange = select(element=plotcontainer).replaceContent(
                loadplot(select(element=selector).getAttr('value')))
            
            return doc

        drawer.mold._createfield_for_sqe = _createfield_for_sqe

        return
    
    pass # end of SQEKernel



from _ import AbstractScatteringKernelInventory as InvBase, sqe_types
class Inventory(InvBase):

    sqe = InvBase.d.reference(
        name = 'sqe',
        targettype=None, targettypes=sqe_types,
        owned = 0,
        )

    Qmin = InvBase.d.float(name = 'Qmin', default = 0)
    Qmax = InvBase.d.float(name = 'Qmax', default = 10)

    Emin = InvBase.d.float(name = 'Emin', default = -50)
    Emax = InvBase.d.float(name = 'Emax', default = 50)
    
    dbtablename = 'sqekernels'
    
    pass # end of Inventory


SQEKernel.Inventory = Inventory
del Inventory
from _ import o2t, KernelTableBase
SQEKernelTable = o2t(
    SQEKernel,
    {'subclassFrom': KernelTableBase},
    )


# version
__id__ = "$Id$"

# End of file 
