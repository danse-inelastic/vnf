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
from luban.content.Splitter import Splitter
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

        # buttons
        buttons = view.document(
            id='%s-table-buttons-container' % name,
            Class='master-table-buttons-container')
        
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
        # filter
        filter_ctrl_container = controls.section(
            id='%s-table-filter-control-container'%name,
            Class = 'master-table-filter-control-container',
            )
        field = FormTextField(
            label = 'Filter: ',
            value = filter_expr,
            id='%s-table-filter' % name,
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

        # toolbar
        toolbar = Splitter(id='%s-table-toolbar'%name, Class='master-table-toolbar')
        view.add(toolbar)
        lefttoolbar = toolbar.section(id='%s-table-toolbar-left' % name, Class='master-table-toolbar-left')
        lefttoolbar.add(controls)
        righttoolbar = toolbar.section(id='%s-table-toolbar-right' % name, Class='master-table-toolbar-right')
        # navigation bar (previous, next...)
        # get a total count
        totalcount = self.countrecords(filter=filter_expr)
        if slice[1] > totalcount: slice[1] = totalcount
        lastpage = (totalcount-1)/number_records_per_page
        # 
        bar = Splitter(
            id='%s-table-navigation-bar'%name,
            Class='master-table-navigation-bar',
            )
        righttoolbar.add(bar)
        #
        first = bar.section(id='%s-table-navigation-bar-first'%name)
        if page_number>0:
            onclick=load(
                actor=name, routine='showListView',
                page_number=0,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr = filter_expr,
                )
            first.add(Link(label='first',onclick=onclick))
        else:
            first.paragraph(text='t', Class='hidden')
        left = bar.section(id='%s-table-navigation-bar-left'%name)
        if page_number>0:
            onclick=load(
                actor=name, routine='showListView',
                page_number=page_number-1,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr = filter_expr,
                )
            left.add(Link(label='previous',onclick=onclick))
        else:
            left.paragraph(text='t', Class='hidden')
        #
        text = '%s-%s of %s' % (slice[0]+1, slice[1], totalcount)
        bar.section(
            id='%s-table-navigation-bar-middle'%name,
            Class='master-table-navigation-bar-middle')\
            .paragraph(text=text)
        #
        right = bar.section(id='matter-table-navigation-bar-right')
        if page_number < lastpage:
            onclick=load(
                actor=name, routine='showListView',
                page_number=page_number+1,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr = filter_expr,
                )
            right.add(Link(label='next',onclick=onclick))
        else:
            right.paragraph(text='t', Class='hidden')
        last = bar.section(id='%s-table-navigation-bar-last'%name)
        if page_number < lastpage:
            onclick=load(
                actor=name, routine='showListView',
                page_number=lastpage,
                number_records_per_page = number_records_per_page,
                order_by = order_by or '',
                reverse_order = reverse_order,
                filter_expr = filter_expr,
                )
            last.add(Link(label='last',onclick=onclick))
        else:
            last.paragraph(text='t', Class='hidden')
        
        # create a table
        table = self.createtable(
            order_by=order_by,
            reverse_order=reverse_order,
            slice=slice,
            filter=filter_expr)
        table.addClass('master-table')
        view.add(table)
        #
        return view



# version
__id__ = "$Id$"

# End of file 
