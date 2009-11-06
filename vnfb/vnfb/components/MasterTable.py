#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from luban.content.FormSelectorField import FormSelectorField
from luban.content.FormTextField import FormTextField
from luban.content.Document import Document
from luban.content.Paragraph import Paragraph
from luban.content.Button import Button
from luban.content.Splitter import Splitter, SplitSection
from luban.content.Toolbar import Toolbar
from luban.content.Link import Link
from luban.content import load, select


import journal


class MasterTableFactory(object):
    
    dummylabel = 'select ...'
    
    def __init__(self, name, countrecords, createtable,
                 compilefilter, filtercols,
                 filterfromlabel, smartlabels, labels,
                 sorting_options=None,
                 polymorphic=True, dbtablename=None,
                 ):
        self.name = name
        self.countrecords = countrecords
        #self.fetchrecords = fetchrecords
        self.createtable = createtable
        
        self.compilefilter = compilefilter
        self.filtercols = filtercols
        
        self.filterfromlabel = filterfromlabel
        self.smartlabels = [self.dummylabel] + smartlabels
        self.labels = labels
        
        self.sorting_options = sorting_options or [
            ('id', 'ID'),
            ('short_description', 'Description'),
            ('type', 'Type'),
            ('date', 'Date created'),
            ]
        
        self.polymorphic = polymorphic
        if not self.polymorphic and not dbtablename:
            raise ProgrammingError, "a non-polymorphic table must supply a table name"
        self.dbtablename = dbtablename
        
        self.debug = journal.debug('MasterTableFactory')
        
        return
    
    
    def create(
        self,
        label=None,
        filter_expr=None, filter_key_index=None, filter_value=None,
        order_by=None, reverse_order=None,
        number_records_per_page=None, page_number=None,
        ):
        name = self.name
        
        view_label = 'View all'

        # the following is to find out the filtering or labeling
        self.debug.log('label: %s' % label)
        if label and label!=self.dummylabel:
            if label in self.smartlabels:
                filter_expr = filter_expr_tocompile = self.filterfromlabel(label)
                view_label = 'collection %r' % label
            else:
                filter_expr_tocompile = None
        else:
            filter_key = self.filtercols[filter_key_index]
            self.debug.log('filter: key:%s, value:%s, expre:%s' % (filter_key, filter_value, filter_expr))
            if filter_expr:
                filter_expr_tocompile = filter_expr
            elif filter_value:
                filter_expr_tocompile = "%s=='%s'" % (filter_key, filter_value)
            else:
                filter_expr_tocompile = None
                
            if filter_expr_tocompile: view_label = filter_expr_tocompile

        # compile filter
        try:
            filter = self.compilefilter(filter_expr_tocompile)
        except:
            raise FilterSyntaxError, filter_expr_tocompile
        
        self.debug.log('compiled filter: %s' % filter)
        
        # parameters
        slice = [page_number*number_records_per_page, (page_number+1)*number_records_per_page]
        
        # create a container
        view = Document(id='%s-list-view' % name, Class='master-table-container')
        
        titlebar = Splitter(Class='master-table-title-bar')
        view.add(titlebar)

        # view indicator
        view_indicator = self.createViewIndicator(name, view_label)
        titlebar.add(view_indicator)
        
        # toolbar with widgets with actions that can change the items in the table
        # such as filtering and creating. sorting and navigating are not such actions
        right = titlebar.section(Class='master-table-toolbar-changeview-container')
        toolbar_changeview = self.createTopToolbar(
            name,
            label,
            filter_expr, filter_key_index, filter_value,
            number_records_per_page,
            order_by, reverse_order,
            )
        right.add(toolbar_changeview)
        
        # sortingtoolbar
        sortingtoolbar = Splitter(
            orientation='horizontal',
            id='%s-table-sortingtoolbar'%name,
            Class = 'master-table-sortingtoolbar')
        self.addSortingControls(
            sortingtoolbar,
            name=name,
            label=label,
            filter_expr=filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
            order_by=order_by, reverse_order=reverse_order,
            number_records_per_page=number_records_per_page,
            )

        # toolbar right on top of table
        tabletoptoolbar = Splitter(id='%s-table-tabletoptoolbar'%name, Class='master-table-tabletoptoolbar')
        view.add(tabletoptoolbar)
        lefttoolbar = tabletoptoolbar.section(id='%s-table-tabletoptoolbar-left' % name, Class='master-table-tabletoptoolbar-left')
        lefttoolbar.add(sortingtoolbar)
        righttoolbar = tabletoptoolbar.section(id='%s-table-tabletoptoolbar-right' % name, Class='master-table-tabletoptoolbar-right')
        # navigation bar (previous, next...)
        bar = self.createNavigationBar(
            name,
            label,
            filter_expr, filter_key_index, filter_value, filter,
            slice, number_records_per_page, page_number,
            order_by, reverse_order,
            'top',
            )
        righttoolbar.add(bar)
        
        # create a table
        table = self.createtable(
            order_by=order_by,
            reverse_order=reverse_order,
            slice=slice,
            filter=filter,
            label=label in self.labels and label or None,
            )
        table.addClass('master-table')
        view.add(table)
        #

        # toolbar right at the bottom of table
        tablebottomtoolbar = Splitter(id='%s-table-tablebottomtoolbar'%name, Class='master-table-tablebottomtoolbar')
        view.add(tablebottomtoolbar)
        lefttoolbar = tablebottomtoolbar.section(id='%s-table-tablebottomtoolbar-left' % name, Class='master-table-tablebottomtoolbar-left')
        collections_toolbar = self.createLabelsToolbar(
            name,
            table=table
            )
        lefttoolbar.add(collections_toolbar)
        
        righttoolbar = tablebottomtoolbar.section(id='%s-table-tablebottomtoolbar-right' % name, Class='master-table-tablebottomtoolbar-right')
        # navigation bar (previous, next...)
        bar = self.createNavigationBar(
            name,
            label,
            filter_expr, filter_key_index, filter_value, filter,
            slice, number_records_per_page, page_number,
            order_by, reverse_order,
            'bottom',
            )
        righttoolbar.add(bar)
        
        return view


    def createViewIndicator(self, name, label):
        view_indicator = SplitSection(id='view-indicator')
        view_indicator.add(Link(label=name.capitalize()+'s', onclick=load(actor=name)))
        view_indicator.paragraph(text=['/ '], Class='splitter')
        view_indicator.paragraph(text=[label])
        return view_indicator


    def createTopToolbar(
        self,
        name,
        label,
        filter_expr, filter_key_index, filter_value,
        number_records_per_page,
        order_by, reverse_order,
        ):

        toolbar_changeview = Toolbar(
            id= '%s-table-toolbar-changeview' % name,
            Class='master-table-toolbar-changeview',
            )
        
        # filter widget
        filter_ctrl_container = self.createFilterWidget(
            name,
            filter_expr, filter_key_index, filter_value,
            number_records_per_page,
            order_by, reverse_order,
            )
        toolbar_changeview.add(filter_ctrl_container)

        # smart label
        smartlabel_widget = self.createSaveSmartLabelWidget(name)
        toolbar_changeview.add(smartlabel_widget)

        # labeled selector
        labeled_widget = self.createCollectionSelectorWidget(
            name,
            label,
            number_records_per_page,
            reverse_order,
            )
        toolbar_changeview.add(labeled_widget)
        
        return toolbar_changeview
    

    def createLabelsToolbar(
        self, name,
        table=None,
        ):
        doc = Document(title='Labels:')

        labels = self.labels
        entries = enumerate(labels)
        field = FormSelectorField(
            #label = 'labeled collections',
            tip = 'choose a label',
            id = '%s-table-applylabel-selector' % name,
            Class='master-table-applylabel-selector',
            entries = entries,
            )
        doc.add(field)
            
        link = Link(label="apply", tip='apply the label to the items you checked')
        doc.add(link)
        
        link.onclick = load(
            actor='label', routine='addEntities', table=name,
            label = select(element=field).formfield('getSelectedLabel'),
            entities = select(element=table).table(
                'getIdentifiersForCheckedRows',
                colname='selected'),
            entity_has_type=self.polymorphic,
            type=self.dbtablename,
            )

        field = FormTextField(tip='input the name of a new label')
        doc.add(field)
        
        link = Link(label='new', tip='click to create a new label')
        doc.add(link)

        link.onclick = load(
            actor='label', routine='new',
            table=name,
            label=select(element=field).getAttr('value'),
            )
            
        link = Link(label='manage', tip='manage my labels')
        doc.add(link)
        link.onclick = load(
            actor='label', routine='manage', table=name,
            )
        return doc


    def createCollectionSelectorWidget(
        self, name,
        label,
        number_records_per_page,
        reverse_order,
        ):

        doc = Document(
            title='Switch to a collection:',
            Class='master-table-labeled-collection-selector-widget')
        
        smartlabels = self.smartlabels
        labels = self.labels
        entries = enumerate(smartlabels+labels)
        field = FormSelectorField(
            #label = 'labeled collections',
            tip='select a collection or a smart collection',
            id='%s-table-collection-selector' % name,
            Class='master-table-collection-selector',
            entries = entries,
            selection = label,
            )
        field.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            order_by = select(id=self._orderByWidgetID(name)).getAttr('value'),
            reverse_order = reverse_order,
            label = select(element=field).formfield('getSelectedLabel'),
            )

        doc.add(field)
        
        return doc


    def createSaveSmartLabelWidget(
        self, name,
        ):

        doc = Document(title='Save search as', Class='master-table-smartlabel-widget')

        field = FormTextField(
            label = '',
            tip='input a name to create a "smart collection" that saves your filtering criteria',
            id='%s-table-smartlabel' % name,
            Class='master-table-smartlabel',
            #tip = "save this search as a smart label",
            )

        createlabel = load(
            actor='smartlabel', routine='create',
            table = name,
            label = select(id=field.id).getAttr('value'),
            filter_expr = select(id=self._filterAdvancedInputFieldID(name)).getAttr('value'),
            filter_key = select(id=self._filterBasicKeyFieldID(name)).formfield('getSelectedLabel'),
            filter_value = select(id=self._filterBasicInputFieldID(name)).getAttr('value'),
            )

        field.onchange = createlabel
        
##         button = Button(
##             label='', icon='label.png', tip='save this search as a smart label',
##             id='smartlabel-button')
##         button.onclick = 

        #doc.add(button)
        doc.add(field)
        
        return doc


    def createFilterWidget(
        self, name,
        filter_expr, filter_key_index, filter_value,
        number_records_per_page,
        order_by, reverse_order,
        ):

        show_advanced_widget = bool(filter_expr)
        
        filter_ctrl_container = Document(
            id='%s-table-filter-control-container'%name,
            Class = 'master-table-filter-control-container',
            title='Filter/search:',
            )

        #filter_ctrl_container.paragraph(
        #    text='Filter/search: ', Class='master-table-filter-label')
            
        advanced = self.createAdvancedFilterWidget(
            name,
            number_records_per_page,
            order_by, reverse_order,
            filter_expr,
            )
        advanced.hidden = not show_advanced_widget
        filter_ctrl_container.add(advanced)

        basic = self.createBasicFilterWidget(
            name,
            filter_key_index, filter_value,
            number_records_per_page,
            order_by, reverse_order,
            )
        basic.hidden = show_advanced_widget
        filter_ctrl_container.add(basic)
        
        return filter_ctrl_container


    def createBasicFilterWidget(
        self, name,
        filter_key_index, filter_value,
        number_records_per_page,
        order_by, reverse_order,
        ):
        basic = Document(
            id=self._basicFilterWidgetID(name),
            Class='master-table-basic-filter-widget',
            )
        
        filtercols = self.filtercols
        entries = enumerate(filtercols)
        selector = FormSelectorField(
            id = self._filterBasicKeyFieldID(name),
            label = 'col:',
            tip = 'select the quantity to filter',
            entries=entries,
            selection=filter_key_index,
            )
        basic.add(selector)

        field = FormTextField(
            label = 'value:',
            tip = 'input a value. wildcard can be use. Eg. *Fe*',
            id = self._filterBasicInputFieldID(name),
            value = filter_value,
            )
        basic.add(field)
        field.onchange =  load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            reverse_order = reverse_order,
            order_by = order_by,
            filter_key_index = select(element=selector).getAttr('value'),
            filter_value = select(element=field).getAttr('value'),
            )
        selector.onchange = select(element=field).setAttr(value='')

        link = Link(label='advanced')
        basic.add(link)
        link.onclick = [
            select(id = self._basicFilterWidgetID(name)).hide(),
            select(id = self._advancedFilterWidgetID(name)).show(),
            ]
        return basic
    
        
    def createAdvancedFilterWidget(
        self, name,
        number_records_per_page,
        order_by, reverse_order,
        filter_expr,
        ):
        
        advanced = Document(
            id=self._advancedFilterWidgetID(name),
            Class='master-table-advanced-filter-widget',
        )
        
        field = FormTextField(
            label = '',
            tip="input a filter expression. Eg. description=='*Fe*'",
            value = filter_expr,
            id=self._filterAdvancedInputFieldID(name),
            Class='master-table-advanced-filter',
            )
        field.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            reverse_order = reverse_order,
            order_by = order_by,
            filter_expr = select(element=field).formfield('getValue'),
            )
        advanced.add(field)

        link = Link(label='basic')
        advanced.add(link)
        link.onclick = [
            select(id = self._basicFilterWidgetID(name)).show(),
            select(id = self._advancedFilterWidgetID(name)).hide(),
            ]
        return advanced


    def addSortingControls(
        self, toolbar,
        name=None,
        label=None,
        filter_expr=None, filter_key_index=None, filter_value=None,
        order_by=None, reverse_order=None,
        number_records_per_page=None,
        ):
        
        # sorting
        sorting_container = toolbar.section(
            id='%s-table-sorting-control-container'%name,
            Class='master-table-sorting-control-container',
            )
        entries = self.sorting_options
        selector = FormSelectorField(
            label = 'Sort by: ',
            entries=entries,
            selection=order_by or '',
            id=self._orderByWidgetID(name),
            )
        selector.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            order_by = select(element=selector).formfield('getSelection'),
            reverse_order = reverse_order,
            filter_expr = filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
            label=label,
            )
        sorting_container.add(selector)
        
        # order reversing
        reverse_order_container = toolbar.section(
            id='%s-table-sorting-reversing-control-container' % name,
            Class = 'master-table-sorting-reversing-control-container',
            )
        entries = [
            ('False', 'Low to High'),
            ('True', 'High to Low'),
            ]
        selector = FormSelectorField(
            label = 'Ordering: ',
            entries=entries,
            selection=reverse_order,
            id='%s-table-reverse_order' % name)
        selector.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            reverse_order = select(element=selector).formfield('getSelection'),
            order_by = order_by,
            filter_expr = filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
            label=label,
            )
        reverse_order_container.add(selector)

        return


    def _orderByWidgetID(self, name):
        return '%s-table-order_by' % name
    def _advancedFilterWidgetID(self, name):
        return '%s-table-advanced-filter-widget' % name
    def _basicFilterWidgetID(self, name):
        return '%s-table-basic-filter-widget' % name
    def _filterAdvancedInputFieldID(self, name):
        return '%s-table-advanced-filter' % name
    def _filterBasicInputFieldID(self, name):
        return '%s-table-basic-filter-value' % name
    def _filterBasicKeyFieldID(self, name):
        return '%s-table-basic-filter-key' % name
    

    def createNavigationBar(
        self, name,
        label,
        filter_expr, filter_key_index, filter_value, filter,
        slice, number_records_per_page, page_number,
        order_by, reverse_order,
        position,
        ):
        
        # get a total count
        totalcount = self.countrecords(filter=filter, label=label!=self.dummylabel and label in self.labels and label or None)
        if slice[1] > totalcount: slice[1] = totalcount
        lastpage = (totalcount-1)/number_records_per_page
        # 
        bar = Document(
            id='%s-table-%s-navigation-bar'%(name, position),
            Class='master-table-navigation-bar',
            )
        #
        if page_number>0:
            id='%s-table-%s-navigation-bar-first'%(name, position)
            onclick=load(
                actor=name, routine='showListView',
                page_number=0,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr=filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
                label=label,
                )
            first = bar.link(id=id, label='first',onclick=onclick)

            bar.paragraph(Class='splitter', text='|')
            
            id='%s-table-%s-navigation-bar-left'%(name, position)
            onclick=load(
                actor=name, routine='showListView',
                page_number=page_number-1,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr=filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
                label=label,
                )
            left = bar.link(id=id, label='previous',onclick=onclick)
        #
        text = '%s-%s of %s' % (slice[0]+1, slice[1], totalcount)
        bar.paragraph(
            id='%s-table-%s-navigation-bar-middle'%(name,position),
            Class='master-table-navigation-bar-middle',
            text=text,
            )
        #
        if page_number < lastpage:
            id='%s-table-%s-navigation-bar-right' % (name, position)
            onclick=load(
                actor=name, routine='showListView',
                page_number=page_number+1,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr = filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
                label=label,
                )
            right = bar.link(id=id,label='next',onclick=onclick)

            bar.paragraph(Class='splitter', text='|')

            id='%s-table-%s-navigation-bar-last'%(name, position)
            onclick=load(
                actor=name, routine='showListView',
                page_number=lastpage,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr=filter_expr, filter_key_index=filter_key_index, filter_value=filter_value,
                label=label,
                )
            last = bar.link(id=id,label='last',onclick=onclick)

        return bar


class FilterSyntaxError(Exception): pass


def filtercompiler(measures, measure2dbcol):
    '''create a compiler that compiles filter expression entered by users to
    a db query expression.

    measures: measures that can be used in user filtering expression. should be a iterable
    measure2dbcol: mapping dictionary to map measure name (used in user filtering expression)
        to db col name.
    '''
    def compilefilter(filter_expr):
        if not filter_expr: return
        from vnfb.utils.safe_eval import safe_eval
        from vnfb.utils.filter import measure as filtermeasure, expr2dbsyntax

        # building the evaluation context
        context = {}
        for measure in measures:
            dbcol = measure2dbcol.get(measure) or measure
            context[measure] = filtermeasure(dbcol)
            continue
        context['expr2dbsyntax'] = expr2dbsyntax
        code = 'expr2dbsyntax(%s)' % filter_expr

        # make sure code is safe
        safe_eval(filter_expr, context=context, check_only=1)

        #
        return expr2dbsyntax(filter_expr, context=context)

    return compilefilter


from luban.components.AuthorizedActor import AuthorizedActor as base
class MasterTableActor(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        
        number_records_per_page = pyre.inventory.int(name='number_records_per_page', default=20)
        page_number = pyre.inventory.int(name='page_number', default=0)
        order_by = pyre.inventory.str(name='order_by', default='id')
        reverse_order = pyre.inventory.bool(name='reverse_order', default=0)
        
        filter_expr = pyre.inventory.str(name='filter_expr')
        filter_key_index = pyre.inventory.int(name='filter_key_index')
        filter_value = pyre.inventory.str(name='filter_value')

        label = pyre.inventory.str(name='label', default='')
        

    def showListView(self, *args, **kwds):
        raise NotImplementedError


    def _init(self):
        super(MasterTableActor, self)._init()
        si = self.inventory
        self._debug.log('label=%s, filter_expr=%s, filter_key_index=%s, filter_value=%s' % (
            si.label, si.filter_expr, si.filter_key_index, si.filter_value) )
        return
    

class ProgrammingError(Exception): pass

# version
__id__ = "$Id$"

# End of file 
