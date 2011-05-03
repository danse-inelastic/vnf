#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



# this is the visual for the whole table view that includes a table and
# many controls.
# it is different from atomicstructure/table which only is the table itself.


from luban.content import load, select, alert
import luban.content



def visual(
    director, name,
    filter_expr=None, filter_key=None, filter_value=None,
    label=None, mine=False,
    order_by=None, reverse_order=None,
    number_records_per_page=None, page_number=None,
    publiconly = False,
    actorname = None
    ):
    """
    name: name of table view
    """
    if actorname is None:
        actorname = name
        
    domaccess = director.retrieveDOMAccessor('atomicstructure')
        
    from vnf.components.MasterTable import MasterTableFactory, filtercompiler
    def countrecords(filter, label=None, mine=False):
        return domaccess.countAtomicStructures(filter, label=label, mine=mine)
    def createtable(order_by, reverse_order, slice, filter, label=None, mine=False):
        return createAtomicStructureTable(
            director, domaccess,
            order_by=order_by,
            reverse_order=reverse_order,
            slice=slice,
            filter=filter,
            label=label,
            mine=mine,
            publiconly = publiconly,
            )
    from vnf.content.visuals.table.atomicstructure import model
    compilefilter = filtercompiler(columns, measure2dbcol, model=model)

    smartlabelaccess = director.retrieveDOMAccessor('smartlabel')
    def filterfromlabel(label):
        return smartlabelaccess.createFilterExprFromLabel(
            label, name)
    smartlabels = smartlabelaccess.getLabelNames(name)

    labelaccess = director.retrieveDOMAccessor('label')
    labels = labelaccess.getLabelNames(name)

    factory = MasterTableFactory(
        name, countrecords, createtable,
        compilefilter, filtercols,
        filterfromlabel, smartlabels, labels,
        sorting_options = [
            # ('id', 'ID'),
            ('short_description', 'Description'),
            ('chemical_formula', 'Chemical formula'),
            ('date', 'Date created'),
        ],
        polymorphic = False, dbtablename='AtomicStructure.Structure',
        publiconly = publiconly,
        )

    tableview = factory.create(
        label = label, mine=mine,
        filter_expr=filter_expr, filter_key=filter_key, filter_value=filter_value,
        order_by=order_by,
        reverse_order=reverse_order,
        number_records_per_page=number_records_per_page,
        page_number=page_number)

    if not publiconly:
        # add new button
        toolbar = tableview.find(id='%s-table-toptoolbar' % name)
        # toolbar.add(Paragraph(text='|', Class='splitter'))
        #
        button = luban.content.button(
            label='New', tip='create new atomic structure', icon='new.png')
        toolbar.add(button)
        button.onclick = select(id='main-display-area').replaceContent(
            load(actor=actorname, routine='newAtomicStructureForm')
            )

    else:
        # add upload button
        toolbar = tableview.find(id='%s-table-toptoolbar' % name)
        #
        button = luban.content.button(
            label='Upload your structure',
            tip='upload your atomic structure',
            icon='new.png',
            Class='big-button',
            )
        toolbar.add(button)
        # the upload view
        uploadview = createPublicUploadView(director)
        button.onclick = select(id='main-display-area')\
            .replaceContent(uploadview)

    return tableview


def createPublicUploadView(director):
    doc = luban.content.document(id='public-upload-structure-container')
    
    vi = viewindicator(director, actorname='atomicstructure-public', this='upload')
    doc.add(vi)
    
    from StructureUploaderFactory import Factory
    f = Factory(
        director=director, 
        oncomplete=('atomicstructure/uploadmatter-public', 'onUpload'),
        )
    doc.add(f.build())
    return doc


# the view indicator to get back to the table view
def viewindicator(director, actorname, this):
    '''actorname: name of the actor to get back to
    this: describe what is current view. a string.
    '''
    #
    path = []
    
    #
    path.append(('Atomic Structures', luban.content.load(actor=actorname)))

        #
    path.append(this)
    
    return director.retrieveVisual('view-indicator', path=path)



def createAtomicStructureTable(
    director, domaccess,
    order_by=None, reverse_order=None, slice=None,
    filter=None,
    label=None,
    mine=False, 
    publiconly = False):

    records = domaccess.getAtomicStructureRecords(
        order_by=order_by, reverse_order=reverse_order, slice=slice,
        filter=filter,
        label=label,
        mine=mine,
        )

    cols = columns
    args = records, cols, director
    if publiconly:
        from vnf.content.visuals.table.atomicstructure_public \
            import table as createTableVisual
    else:
        from vnf.content.visuals.table.atomicstructure \
            import table as createTableVisual
    thetable = createTableVisual(
        records, cols, director)
    thetable.oncellchanged = select(element=thetable).notify(
        event='row-changed', actor='atomicstructure/table', routine='processRowChange')
    return thetable



columns = [ 'selected', 'id', 'description', 'chemical_formula', 'creator', 'created']
measure2dbcol = {
    'description': 'short_description',
    'created': 'date',
    }
filtercols = columns[2:]


# version
__id__ = "$Id$"

# End of file 
