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


from AbstractNeutronComponent import AbstractNeutronComponent as base
class NeutronPlayer(base):

    abstract = False

    neutrons = None
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'neutrons',
            ]
        drawer.sequence = ['properties']

        def _createfield_for_neutrons(obj):
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
            referred_record = record.neutrons and record.neutrons.id \
                              and record.neutrons.dereference(self.orm.db)

            # widget
            doc = lc.document(Class='container', id='neutrons-selector-container')
            sp = doc.splitter(orientation='horizontal')
            left = sp.section(); right = sp.section()
            #
            selector = FormSelectorField(label='Neutrons:', name='neutrons')
            left.add(selector)
            #
            viewcontainer = right.document(Class='container')
            #
            loadview = lambda uid: load(
                actor='orm/neutronstorages', routine='createGraphicalView',
                uid=uid, start=0, end=2)

            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
                viewcontainer.oncreate = select(element=viewcontainer).append(
                    loadview(value))
            else:
                value=None

            # choices
            #  dynamically load choices
            entries = load(
                actor='orm/neutronplayers',
                routine='getSelectorEntriesForReference',
                refname = 'neutrons',
                include_none_entry = 1,
                )
            selector.oncreate = select(element=selector).setAttr(entries=entries, value=value)
            selector.onchange = select(element=viewcontainer).replaceContent(
                loadview(select(element=selector).getAttr('value')))
            
            return doc

        drawer.mold._createfield_for_neutrons = _createfield_for_neutrons
        
    pass



from vnf.dom.neutron_experiment_simulations.NeutronStorage import NeutronStorage

InvBase=base.Inventory
class Inventory(InvBase):

    neutrons = InvBase.d.reference(name='neutrons', targettype=NeutronStorage, owned=False)
    dbtablename = 'neutronplayers'



NeutronPlayer.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase as TableBase
NeutronPlayerTable = o2t(NeutronPlayer, {'subclassFrom':TableBase})


# version
__id__ = "$Id$"

# End of file 
