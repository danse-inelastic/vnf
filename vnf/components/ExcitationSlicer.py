#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


class ExcitationSlicer(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'excitationSlicer' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        username = director.sentry.username
        userrecord = director.clerk.getUser( username )
        fullname = userrecord.fullname
        title = 'Welcome to the Virtual Neutron Facility, %s!' % (
            fullname,),
        document = main.document(title=title)
        
        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = 'run virtual neutron experiments', routine = 'default',
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'In this web service facility, you can %s. ' % link,
            'In a virtual neutron experiment, ',
            'virtual neutrons are generated from a virtual neutron moderator,',
            'guided by virtual neutron guides,',
            'scattered by a virtual sample and sample environment,',
            'and intercepted by detectors.',
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'instrument', sentry = director.sentry,
            label = 'neutron instruments', routine = 'listall',
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You can do your experiments on a variety of %s,' % link,
            'both actual physical instruments and conceptual, nonphysical instruments'
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'scatteringKernel', sentry = director.sentry,
            label = 'scattering kernels', routine = 'default',
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You can also create your sample and predict its neutron',
            'scattering properties by calculating its structure or dynamics.',
            'For example, the material behaviors calculated by ab initio'
            'or molecular dynamics methods become',
            '%s that can be used in the sample simulation' % link,
            'part of your virtual experiment.',
            ]

        p = document.paragraph()
        p.text = [
            'On the left, several menu items link to a variety of',
            'functions.',
            'You can review past experiments by clicking "Experiments",',
            'or browse your personal library of sample assemblies by',
            'clicking "Sample Assemblies".',
            'Neutron instruments in which you can run your experiments',
            'are accessible through "Instruments".',
            'When you start a virtual experiment, or a material',
            'simulation, they became jobs submitted to computing',
            'resources. You can monitor their progress by clicking',
            '"Jobs".',
            ]

        p = document.paragraph()
        email = '<a href="mailto:danse-inelastic@cacr.caltech.edu">us</a>'
        p.text = [
            'We welcome your comments on this web service, ',
            'suggestions for new features, and reports of',
            'discrepancies or bugs.'
            ]

        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(Greeter, self).__init__(name)
        return


    pass # end of Greeter


# version
__id__ = "$Id$"

# End of file 
