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
from luban.content.Splitter import Splitter
from luban.content.Toolbar import Toolbar
from luban.content.Link import Link
from luban.content import load, select


class MasterTableFactory(object):

    
    def __init__(self, name, countrecords, createtable):
        self.name = name
        self.countrecords = countrecords
        #self.fetchrecords = fetchrecords
        self.createtable = createtable
        return
    

    def create(self, order_by=None, reverse_order=None, filter_expr=None,
               number_records_per_page=None, page_number=None,
               sorting_options=None,
               ):
        name = self.name
        
        # parameters
        slice = [page_number*number_records_per_page, (page_number+1)*number_records_per_page]
        
        # create a container
        view = Document(id='%s-list-view' % name)
        
        splitter = Splitter(Class='master-table-title-bar')
        view.add(splitter)
        view_indicator = splitter.section(id='view-indicator')
        view_indicator.add(Link(label=name.capitalize()+'s', onclick=load(actor=name)))
        view_indicator.paragraph(text=['/ '], Class='splitter')
        if filter_expr:
            text = filter_expr
        else:
            text = 'View all'
        view_indicator.paragraph(text=[text])
        
        # toolbar with widgets with actions that can change the items in the table
        # such as filtering and creating. sorting and navigating are not such actions
        right = splitter.section(Class='master-table-toolbar-changeview-container')
        toolbar_changeview = Toolbar(
            id= '%s-table-toolbar-changeview' % name,
            Class='master-table-toolbar-changeview',
            )
        right.add(toolbar_changeview)
        
        # filter widget
        filter_ctrl_container = self.createFilterWidget(
            name,
            number_records_per_page,
            order_by, reverse_order,
            filter_expr,
            )
        toolbar_changeview.add(filter_ctrl_container)

        # smart label
        smartlabel_widget = self.createSmartLabelWidget(name)
        toolbar_changeview.add(smartlabel_widget)
        
        # controls
        controls = Splitter(
            orientation='horizontal',
            id='%s-table-controls'%name,
            Class = 'master-table-controls')
        # sorting
        sorting_container = controls.section(
            id='%s-table-sorting-control-container'%name,
            Class='master-table-sorting-control-container',
            )
        if sorting_options is None:
            entries = [
                ('id', 'ID'),
                ('short_description', 'Description'),
                ('type', 'Type'),
                ('date', 'Date created'),
                ]
        else:
            entries = sorting_options
        selector = FormSelectorField(
            label = 'Sort by: ',
            entries=entries,
            selection=order_by or '',
            id='%s-table-order_by' % name,
            )
        selector.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            order_by = select(element=selector).formfield('getSelection'),
            reverse_order = reverse_order,
            filter_expr = filter_expr,
            )
        sorting_container.add(selector)
        # order reversing
        reverse_order_container = controls.section(
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
            filter_expr = filter_expr,
            )
        reverse_order_container.add(selector)

        # toolbar right on top of table
        toolbar = Splitter(id='%s-table-toolbarontop'%name, Class='master-table-toolbarontop')
        view.add(toolbar)
        lefttoolbar = toolbar.section(id='%s-table-toolbarontop-left' % name, Class='master-table-toolbarontop-left')
        lefttoolbar.add(controls)
        righttoolbar = toolbar.section(id='%s-table-toolbarontop-right' % name, Class='master-table-toolbarontop-right')
        # navigation bar (previous, next...)
        bar = self.createNavigationBar(
            name,
            slice, number_records_per_page, page_number,
            order_by, reverse_order,
            filter_expr,
            'top',
            )
        righttoolbar.add(bar)
        
        # create a table
        table = self.createtable(
            order_by=order_by,
            reverse_order=reverse_order,
            slice=slice,
            filter=filter_expr)
        table.addClass('master-table')
        view.add(table)
        #

        # toolbar right at the bottom of table
        toolbar = Splitter(id='%s-table-toolbaronbottom'%name, Class='master-table-toolbaronbottom')
        view.add(toolbar)
        lefttoolbar = toolbar.section(id='%s-table-toolbaronbottom-left' % name, Class='master-table-toolbaronbottom-left')
        righttoolbar = toolbar.section(id='%s-table-toolbaronbottom-right' % name, Class='master-table-toolbaronbottom-right')
        # navigation bar (previous, next...)
        bar = self.createNavigationBar(
            name,
            slice, number_records_per_page, page_number,
            order_by, reverse_order,
            filter_expr,
            'bottom',
            )
        righttoolbar.add(bar)
        
        return view


    def createSmartLabelWidget(
        self, name,
        ):

        doc = Document()

        field = FormTextField(
            label = '',
            id='%s-table-smartlabel' % name,
            Class='master-table-smartlabel',
            )

        button = Button(
            label='', icon='label.png', tip='save this search as a smart label',
            id='smartlabel-button')
        button.onclick = load(
            actor='smartlabel', routine='create',
            table = name,
            label = select(id=field.id).getAttr('value'),
            fitler_expr = select(id=self._filterInputFieldID(name)).getAttr('value'),
            )

        doc.add(button)
        doc.add(field)
        
        return doc


    def createFilterWidget(
        self, name,
        number_records_per_page,
        order_by, reverse_order,
        filter_expr,
        ):

        filter_ctrl_container = Document(
            id='%s-table-filter-control-container'%name,
            Class = 'master-table-filter-control-container',
            )
        
        field = FormTextField(
            label = 'Filter/search: ',
            value = filter_expr,
            id=self._filterInputFieldID(name),
            Class='master-table-filter',
            )
        field.onchange = load(
            actor=name, routine='showListView',
            number_records_per_page = number_records_per_page,
            page_number = 0,
            reverse_order = reverse_order,
            order_by = order_by,
            filter_expr = select(element=field).formfield('getValue'),
            )
        filter_ctrl_container.add(field)
        
        return filter_ctrl_container


    def _filterInputFieldID(self, name):
        return '%s-table-filter' % name
    

    def createNavigationBar(
        self, name,
        slice, number_records_per_page, page_number,
        order_by, reverse_order,
        filter_expr,
        position,
        ):
        
        # get a total count
        totalcount = self.countrecords(filter=filter_expr)
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
                filter_expr = filter_expr,
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
                filter_expr = filter_expr,
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
                filter_expr = filter_expr,
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
                filter_expr = filter_expr,
                )
            last = bar.link(id=id,label='last',onclick=onclick)

        return bar



# version
__id__ = "$Id$"

# End of file 
