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


def login(actor, username='selenium', password='demo'):
    
    usernamei = actor.select(type = 'formtextfield', id='login-username-input')
    passwordi = actor.select(type = 'formtextfield', id='login-password-input')
    
    usernamei.type(username)
    passwordi.type(password)
    
    submit = actor.select(type = 'formsubmitbutton', id='login-submitbutton')
    submit.click()
    
    minimize = actor.select(type='button', id='minimize-help-button')
    minimize.click()
    
    return



def basic_filter(actor, table, key, value):
    select = actor.select(
        type='formselectorfield', 
        id='%s-table-basic-filter-key' % table,
        )
    select.select(key)

    filterexpr_input = actor.select(
        type = 'formtextfield',
        id = '%s-table-basic-filter-value' % table,
        )
    filterexpr_input.type(value)
    return
        


# version
__id__ = "$Id$"

# End of file 
