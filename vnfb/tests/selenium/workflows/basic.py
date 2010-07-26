#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def login(s, username='demo', password='demo'):
    usernamei = "//div[@id='login-username-input']"
    passwordi = "//div[@id='login-password-input']"
    inputsubelem = '/table/tbody/tr/td[1]/input'
    s.waitForElementPresent(usernamei)
    s.type(usernamei+inputsubelem, username)
    s.type(passwordi+inputsubelem, password)

    submit = "//input[@type='submit']"
    s.click(submit)

    minimize = "//div[@id='minimize-help-button']/a/span"
    s.waitForElementPresent(minimize)
    s.click(minimize)
    return



def basic_filter(s, table, key, value):
    select = s.lh.formfield('%s-table-basic-filter-key' % table, 'select')
    s.select(select, key)
    s.type(s.lh.formfield('%s-table-basic-filter-value' % table, 'input'),
           value)
    return
        


# version
__id__ = "$Id$"

# End of file 
