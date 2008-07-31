#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## this is an example given by Michael (from ent)

from Actor import Actor


class Purser(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"

        order = pyre.inventory.str("order", default="date")
        order.meta['tip'] = "the field to sort the outstanding expenses by"

        amount = pyre.inventory.str("amount")
        amount.meta['tip'] = "the amount of an expense entry"

        category = pyre.inventory.str("category")
        category.meta['tip'] = "the category for an expense entry"

        code = pyre.inventory.str("code", default="VISA 001")
        code.meta['tip'] = "the charge code for an expense entry"

        date = pyre.inventory.str("date", default=time.strftime("%Y/%m/%d"))
        date.meta['tip'] = "the date of an expense entry"

        description = pyre.inventory.str("description")
        description.meta['tip'] = "the description of an expense entry"

        location = pyre.inventory.str("location")
        location.meta['tip'] = "the location code for an expense entry"

        expenses = pyre.inventory.list(name="expenses")


    def default(self, director):
        return self.expenses(director)


    def expenses(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._outstandingExpenses(director, content)
        return page


    def new(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._collectNewExpense(director, content)
        return page


    def edit(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._editExpense(director, content)
        return page


    def delete(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._deleteExpense(director, content)
        return page


    def submitExpenseReport(self, director, page=None):
        if not page:
            page = director.retrieveSecurePage("expenses")

        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._submitExpenseReport(director, content)
        return page


    def viewExpenseReport(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._viewExpenseReport(director, content)
        return page


    def confirmDelete(self, director):
        self._removeExpense(director)

        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._outstandingExpenses(director, content)
        return page


    def confirmExpenseReport(self, director, page=None):
        username = director.sentry.username
        confirmation = director.idd.token().locator
        expenses = self.inventory.expenses

        if not page:
            page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        if not expenses:
            section = content.document(title="Missing expenses")
            p = section.paragraph(cls="error")
            p.text = [
                "You cannot submit an empty expense report. Please select some expenses",
                "and try again."
                ]
            return self.submitExpenseReport(director, page)

        director.clerk.submitExpenseReport(confirmation, username, expenses)

        section = content.document(title="Success")

        p = section.paragraph()
        p.text = [
            "Your expense report has been submitted successfully.",
            "Your confirmation code is <strong>%s</strong>." % confirmation
            ]

        return page


    def submit(self, director):
        import time

        errors = {}

        # get the application context
        idd = director.idd
        clerk = director.clerk
        username = director.sentry.username

        # collect the data
        tag = self.inventory.id
        amount = self.inventory.amount
        category = self.inventory.category
        code = self.inventory.code
        date = self.inventory.date
        description = self.inventory.description

        # validate
        if not code:
            errors["code"] = "Please make sure you select a valid project code"

        if not category:
            errors["category"] = "Please make sure you select a valid expense category"

        if not amount:
            errors["amount"] = "Please enter an amount; this field may not be left blank"
        else:
            try:
                expenseAmount = float(amount.strip())
            except ValueError:
                errors["amount"] = (
                    "Invalid amount: please use only digits and decimal points in this field")

        if not code:
            errors["code"] = "Please make sure you select a valid project code"

        if not category:
            errors["category"] = "Please make sure you select a valid expense category"

        # repair the date input
        # apparently some browsers screw this one up
        date = '%4d/%02d/%02d' % tuple(map(int, date.split('/')))

        #if not description:
            #errors["description"] = (
                #"Please enter a description for this expense"
                #)

        # see whether we need to collect corrections from the user
        if errors:
            page = director.retrieveSecurePage("expenses")
            if not page:
                return director.retrievePage("authentication-error")
        
            content = page._body._content._main
            self._collectNewExpense(director, content, errors=errors, new=False)
            return page

        # all ok: create the Expense object
        from ent.dom.Expense import Expense
        expense = Expense()

        if not tag:
            expense.id = idd.token().locator
        else:
            expense.id = tag
        expense.employee = username
        expense.date = date
        expense.submitted = time.strftime("%Y/%m/%d")
        expense.code = code
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.status = 'n'

        # if we are updating, do it and show the main page
        if tag:
            clerk.updateExpense(expense)
            return self.expenses(director)
        
        # this is a new expense
        clerk.newExpense(expense)
        
        # build the page shell
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main

        # report success
        section = content.document(title='Success')
        p = section.paragraph(cls="success")
        p.text = [
            "Your expense has been submitted. You may now enter another one",
            "by filling out the form below, or you can",
            "use the expense menu on the left to navigate to another part of the application."
            ]
        p = section.paragraph()
        p.text = [
            "Here is a summary of the information you entered:"
            ]

        p = section.paragraph()
        p.text = [
            "Expense code: &nbsp;&nbsp;<b>%s</b><br>" % expense.id,
            "amount: &nbsp;&nbsp;<b>%s</b><br>" % expense.amount,
            "date: &nbsp;&nbsp;<b>%s</b><br>" % expense.date,
            "description: &nbsp;&nbsp;<b>%s</b><br>" % expense.description,
            "project: &nbsp;&nbsp;<b>%s</b><br>" % expense.code,
            "category: &nbsp;&nbsp;<b>%s</b><br>" % expense.category,
            "submitted by: &nbsp;&nbsp;<b>%s</b><br>" % expense.employee,
            "submitted on: &nbsp;&nbsp;<b>%s</b><br>" % expense.submitted,
            ]

        # add the expense collection form in case they want to submit another one
        self._collectNewExpense(director, content)

        return page


    def view(self, director):
        page = director.retrieveSecurePage("expenses")
        if not page:
            return director.retrievePage("authentication-error")
        
        content = page._body._content._main
        self._listExpenseReports(director, content)
        return page


    def __init__(self, name=None):
        if name is None:
            name = "purser"
        super(Purser, self).__init__(name)
        return


    def _collectNewExpense(self, app, content, errors={}, new=True):
        # get access to the app context
        scribe = app.scribe

        section = content.document(title='Enter a new expense')
        p = section.paragraph()
        p.text = [
            "Use the fields below to enter your expense information"
            ]

        scribe.expenseForm(self.name, app, section, self.inventory, errors, new)

        return


    def _removeExpense(self, app):
        # get access to the app context
        clerk = app.clerk
        clerk.deleteExpense(self.inventory.id)

        return


    def _deleteExpense(self, app, content):
        # get access to the app context
        clerk = app.clerk
        scribe = app.scribe

        expense = clerk.retrieveExpense(self.inventory.id)

        section = content.document(title='Delete a submitted expense')
        p = section.paragraph()
        p.text = [
            "You are attempting to delete the following expense record:"
            ]
        
        # generate the table
        table = section.literal()
        text = [
            '<p>',
            '<table cellspacing="0" class="expenseTable">',
            '  <thead>',
            '    <tr class="expenseHeader">',
            '      <th>Date</th>',
            '      <th>Code</th>',
            '      <th>Category</th>',
            '      <th>Description</th>',
            '      <th>Amount</th>',
            '    </tr>',
            '  </thead>',
            '  <tbody>',
            ]

        description = expense.description
        if not description:
            description = "&nbsp;"
        text += [
            '    <tr class="even">',
            '      <td class="expenseDate">%s</td>' % expense.date,
            '      <td class="expenseCode">%s</td>' % expense.code,
            '      <td class="expenseCategory">%s</td>' % expense.category,
            '      <td class="expenseDescription">%s</td>' % description,
            '      <td class="expenseAmount">$%-9.2f</td>' % expense.amount,
            '    </tr>',
            ]

        text += [
            '  </tbody>',
            '</table>',
            '</p>',
            ]

        table.text = text

        actions = [
            "actor=purser",
            "routine=confirmDelete",
            "purser.id=%s" % self.inventory.id,
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket
            ]
        confirm = '<a href="%s?%s">confirm</a>' % (app.cgihome, "&".join(actions))

        actions = [
            "actor=purser",
            "routine=expenses",
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket
            ]
        cancel = '<a href="%s?%s">cancel</a>' % (app.cgihome, "&".join(actions))

        p = section.paragraph()
        p.text = [
            "Please",
            confirm,
            "that this is what you really want or",
            cancel,
            "this operation and return to the main page."
            ]
        
        return


    def _editExpense(self, app, content):
        # get access to the app context
        clerk = app.clerk
        scribe = app.scribe

        expense = clerk.retrieveExpense(self.inventory.id)

        section = content.document(title='Modify a submitted expense')
        actions = [
            "actor=purser",
            "routine=delete",
            "purser.id=%s" % self.inventory.id,
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket,
            ]
        p = section.paragraph()
        p.text = [
            'Use the fields below to make any changes to your expense information or',
            'you may',
            '<a href="%s?%s">delete</a>' % (app.cgihome, "&".join(actions)),
            'it.'
            ]

        scribe.expenseForm(self.name, app, section, expense, new=False)

        return


    def _submitExpenseReport(self, app, content):
        # get the outstanding expenses
        expenses = app.clerk.retrieveOutstandingExpenses(
            username=app.sentry.username, order=self.inventory.order)

        section = content.document(title='Submit an expense report')
        p = section.paragraph()
        if not expenses:
            p.text = [
                "You have no outstanding expenses."
                ]
            return

        p = section.paragraph()
        p.text = [
            "You have selected to submit an expense report based on your outstanding",
            "expenses listed in the table below."
            ]

        app.scribe.renderExpenses(
            director=app, actor=self.name, routine="submitExpenseReport",
            document=section,
            expenses=expenses,
            editable=False, selectable=True, sortable=True)

        actions = [
            "actor=purser",
            "routine=expenses",
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket
            ]
        cancel = '<a href="%s?%s">cancel</a>' % (app.cgihome, "&".join(actions))

        p = section.paragraph()
        p.text = [
            "If you don't want to submit this expense report, you can",
            cancel,
            "this operation and return to the main page."
            ]
        
        return


    def _viewExpenseReport(self, app, content):
        reportId = self.inventory.id
        report = app.clerk.retrieveExpenseReport(reportId)
        expenses = app.clerk.retrieveReportedExpenses(reportId)

        section = content.document(title="Expense detail")

        if not expenses:
            p = section.paragraph()
            p.text = [
                "This expense report contains no actual reported expenses"
                ]
            return

        p = section.paragraph()
        p.text = [
            "Here are the expenses that were part of expense report",
            "<strong>%s</strong>," % reportId,
            "submitted on %s:" % report.submitted
            ]

        app.scribe.renderExpenses(
            director=app, actor=self.name, routine="viewExpenseReport",
            document=section, expenses=expenses, editable=False, sortable=False)
            
        import os
        home, script = os.path.split(app.cgihome)
        retriever = os.path.join(home, "archive.py")
        args = [
            "actor=archiver",
            "routine=expenseDetail",
            "actor.document=%s" % reportId,
            "actor.format=%s",
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket,
            ]
        link = "%s?%s" % (retriever, "&".join(args))

        p = section.paragraph()
        p.text = [
            "You can download this report as a",
            '<a href="%s">CSV</a>' % (link % "csv"),
            "file, suitable for importing into",
            "spreadsheet applications, such as Microsoft Excel."
            ]

        return


    def _outstandingExpenses(self, app, content):
        # get the user's handle
        username = app.sentry.username

        # list the outstanding expenses if any
        section = content.document(title='Summary of outstanding expenses')
        p = section.paragraph()
        p.text = [
            "You may enter new expenses or submit a new expense report",
            "by selecting from the menu on the left."
            ]
        expenses = app.clerk.retrieveOutstandingExpenses(username, self.inventory.order)
        if not expenses:
            p = section.paragraph()
            p.text = [
                "You have no outstanding expenses."
                ]
            return

        # grab the charge codes and their descriptions
        codes = app.clerk.indexProjects()

        # index the expenses by charge code
        summary = {}
        for expense in expenses:
            amount = summary.setdefault(expense.code, 0.0)
            amount += expense.amount
            summary[expense.code] = amount
            
        p = section.paragraph()
        p.text = [
            "The following table contains a summary of outstanding expenses you have",
            "entered by project charge code."
            ]
        app.scribe.renderExpenseSummaryByChargeCode(app, section, codes, summary)

        p = section.paragraph()
        p.text = [
            "The following table lists outstanding expenses you have entered into the system",
            "that have not been submitted as part of an expense report. You may modify",
            "any of these entries by following the associated link in the first column",
            "of the table."
            ]

        app.scribe.renderExpenses(
            director=app,
            actor=self.name, routine="expenses",
            document=section, expenses=expenses, sortable=True)

        return


    def _listExpenseReports(self, app, content):
        # get the user's handle
        username = app.sentry.username

        # create the document
        section = content.document(title='Submitted expense reports')

        # get the expense reports
        reports = app.clerk.retrieveExpenseReports("employee='%s'" % username)

        if not reports:
            p = section.paragraph()
            p.text = [
                "You have not submitted any expense reports."
                ]
            return

        p = section.paragraph()
        p.text = [
            "The following table lists all the expense reports you have submitted.",
            "You can view the associated expense detail by following the link in the",
            "first column of the table."
            ]

        # get the employee index so we can find the employee's full name
        employees = app.clerk.indexEmployees()
        fullname = employees[username].fullname

        # render the table
        actions = [
            "actor=purser",
            "routine=viewExpenseReport",
            "purser.id=%s", # placeholder for the report id
            "sentry.username=%s" % app.sentry.username,
            "sentry.ticket=%s" % app.sentry.ticket,
            ]
        app.scribe.renderUserExpenseReports(app, section, fullname, reports, actions)
        
        return


# version
__id__ = "$Id: Purser.py,v 1.7 2007-11-29 09:28:36 aivazis Exp $"

# End of file 
