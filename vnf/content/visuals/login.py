# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# this is the factory for the page containing login form
# and also introductory materials


from luban.content import load, select, alert, createCredential
import luban.content as lc


class Factory(object):


    def createFrame(self, post_authorization_action='', director=None):
        visual = self.createFrontPageContent(
            post_authorization_action, director)
        
        frame = lc.frame(title='Virtual neutron facility: please login')
        frame.add(visual)

        dock = lc.dock(id='dock', hidden=True)
        frame.add(dock)
        
        return frame
    
    
    def createFrontPageContent(self, post_authorization_action, director):
        '''create the content of the front page (frame)
        add it to a frame then we have the login frame
        '''
        skeleton = director.retrieveVisual('skeleton')

        # hide userinfo
##         header = skeleton.find(id='mainframe-header')
##         userinfo = header.find(id='header-userinfo')
##         userinfo.hidden = True

        # the content
        body_frame = skeleton.find(id='body-frame')
        body = self.createFrontPageBodyDocument(
            post_authorization_action, director)
        body_frame.add(body)
        
        return skeleton


    def createFrontPageBodyDocument(self, post_authorization_action, director):
        '''create the body document for the front page
        embed this document inside the skeleton in visuals/skeleton then we
        get the whole front page (frame)
        '''
        bodydoc = lc.document(id='login-body-doc')
        splitter = lc.splitter(id='login-body-splitter')
        bodydoc.add(splitter)

        # left
        left = splitter.section(id='login-body-left')
        # form
        formcontainer = left.document(id='login-form-container')
        form = director.retrieveVisual(
            'login-form', 
            post_authorization_action=post_authorization_action)
        formcontainer.add(form)
        # portlet
        portlet = director.retrieveVisual('frontpage-portlet')
        left.add(portlet)
        #

        # right
        right = splitter.section(id='login-body-right')
        # introduction
        introcontainer = right.document(
            id='front-page-vnf-intro-container',
            title='Welcome to the Virtual Neutron Facility',
            )
        intro = lc.htmldocument(); introcontainer.add(intro)
        intro.text = [
            #'The Virtual Neutron Facility (VNF) provides online computation tools for simulating neutron scattering experiments.',
            '<p>The Virtual Neutron Facility (VNF) is an online tool that allows users to perform end-to-end, full simulations of neutron scattering experiments. It integrates scientific software packages for material simulations with Monte-Carlo simulations of neutron scattering to gain insights into material properties.</p>',
            ]
        # central display
        ctrldisplay = right.document(id='front-page-central-display')
        initialviewdocuments = [
            'screencasts',
            #'tutorials',
            'status',
            'technology',
            #'personnel',
            ]
        for idoc in initialviewdocuments:
            doc = director.redirect(
                actor='frontpage', routine='createDocument', name=idoc,
                include_credential=False)
            doc.Class += ' alternating-bg'
            ctrldisplay.add(doc)
            continue
        # footnote
        footnotecontainer = right.document(id='front-page-footnote-container')
        htmldoc = lc.htmldocument(); footnotecontainer.add(htmldoc)
        htmldoc.text = [
            'The VNF is a product of the <a target="_blank" href="http://danse.us">DANSE</a> project, which is bringing computational materials science and instrument simulations to neutron scattering experiments. The  DANSE project is funded by the US National Science Foundation under grant DMR-0520547.',
            ]
        htmldoc = lc.htmldocument(); footnotecontainer.add(htmldoc)
        htmldoc.text = [        
            # 'You are presently at the stable release site of VNF; the version under development is <a target="_blank" href="https://vnf-dev.caltech.edu">here</a>.',
            'You are presently at the development site of VNF; the release sites of vnf are available at <a target="_blank" href="https://vnf.caltech.edu">caltech</a> and <a target="_blank" href="https://vnf.sns.gov">SNS</a> (the latter is only accessible from inside ORNL)',
            ]
        return bodydoc



# version
__id__ = "$Id$"

# End of file 
