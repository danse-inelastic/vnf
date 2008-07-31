#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from Actor import Actor


class Recruiter(Actor):


    class Inventory(Actor.Inventory):

        import pyre.inventory

        cid = pyre.inventory.str(name="cid")
        lastname = pyre.inventory.str(name="lastname")
        firstname = pyre.inventory.str(name="firstname")

        address = pyre.inventory.str(name="address")
        city = pyre.inventory.str(name="city")
        state = pyre.inventory.str(name="state")
        postal = pyre.inventory.str(name="postal")
        country = pyre.inventory.str(name="country")

        phone = pyre.inventory.str(name="phone")
        email = pyre.inventory.str(name="email")

        position = pyre.inventory.str(name="position")
        office = pyre.inventory.str(name="office")
        startMonth = pyre.inventory.str(name="startMonth")
        startYear = pyre.inventory.str(name="startYear")
        referral = pyre.inventory.str(name="referral")

        degree_1 = pyre.inventory.str(name="degree_1")
        field_1 = pyre.inventory.str(name="field_1")
        school_1 = pyre.inventory.str(name="school_1")
        graduationMonth_1 = pyre.inventory.str(name="graduationMonth_1")
        graduationYear_1 = pyre.inventory.str(name="graduationYear_1")
        
        degree_2 = pyre.inventory.str(name="degree_2")
        field_2 = pyre.inventory.str(name="field_2")
        school_2 = pyre.inventory.str(name="school_2")
        graduationMonth_2 = pyre.inventory.str(name="graduationMonth_2")
        graduationYear_2 = pyre.inventory.str(name="graduationYear_2")
        
        degree_3 = pyre.inventory.str(name="degree_3")
        field_3 = pyre.inventory.str(name="field_3")
        school_3 = pyre.inventory.str(name="school_3")
        graduationMonth_3 = pyre.inventory.str(name="graduationMonth_3")
        graduationYear_3 = pyre.inventory.str(name="graduationYear_3")
        
        company_1 = pyre.inventory.str(name="company_1")
        position_1 = pyre.inventory.str(name="position_1")
        city_1 = pyre.inventory.str(name="city_1")
        country_1 = pyre.inventory.str(name="country_1")
        startMonth_1 = pyre.inventory.str(name="startMonth_1")
        startYear_1 = pyre.inventory.str(name="startYear_1")
        endMonth_1 = pyre.inventory.str(name="endMonth_1")
        endYear_1 = pyre.inventory.str(name="endYear_1")
        
        company_2 = pyre.inventory.str(name="company_2")
        position_2 = pyre.inventory.str(name="position_2")
        city_2 = pyre.inventory.str(name="city_2")
        country_2 = pyre.inventory.str(name="country_2")
        startMonth_2 = pyre.inventory.str(name="startMonth_2")
        startYear_2 = pyre.inventory.str(name="startYear_2")
        endMonth_2 = pyre.inventory.str(name="endMonth_2")
        endYear_2 = pyre.inventory.str(name="endYear_2")
        
        company_3 = pyre.inventory.str(name="company_3")
        position_3 = pyre.inventory.str(name="position_3")
        city_3 = pyre.inventory.str(name="city_3")
        country_3 = pyre.inventory.str(name="country_3")
        startMonth_3 = pyre.inventory.str(name="startMonth_3")
        startYear_3 = pyre.inventory.str(name="startYear_3")
        endMonth_3 = pyre.inventory.str(name="endMonth_3")
        endYear_3 = pyre.inventory.str(name="endYear_3")
        
        cover = pyre.inventory.str(name="cover")
        resume = pyre.inventory.str(name="resume")


    def welcome(self, director):
        page = director.retrievePage("recruiting")

        content = page._body._content._main
        section = content.document(
            title='Welcome to the OC&amp;C Online Application Submission Site')

        p = section.paragraph()
        p.text = [
            "Thank you for your interest in OC&amp;C Strategy Consultants.",
            "Please complete this online application for consulting positions",
            "at any of the US offices of OC&amp;C.",
            "The application form collects basic contact information, education and",
            "work history, as well as a resume and cover letter."
            ]
        
        p = section.paragraph()
        p.text = [
            "The information you provide will be considered confidential.",
            "OC&amp;C will not this information for any purpose other than to evaluate",
            "your candidacy for present or future positions.",
            "By submitting this application, you acknowledge that",
            "OC&amp;C Strategy Consultants will have access to the application information",
            "for such purposes, and you consent to such use, including the transmission",
            "of this information to affiliates worldwide."
            ]

        p = section.paragraph()
        p.text = [
            "If you encounter any errors during the submission of your application,",
            "or you cannot successfully complete all the required steps,",
            "please send an email to",
            "<b>recruiting</b>&nbsp;@&nbsp;<b>occstrategy.us</b>"
            ]

        p = section.paragraph(cls="success")
        p.text = [
            "If you have submitted any part of your application before and cannot remember",
            "your candidate ID, please do not start a new application.",
            "Just send an email to",
            "<b>recruiting</b>&nbsp;@&nbsp;<b>occstrategy.us</b>",
            "and we will retrieve it for you.",
            ]

        # handle new applications
        import ent.content
        form = section.form(
            name="new_applicant",
            legend="New applicants:",
            action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="newApplicant")

        p = form.paragraph()
        p.text = [
            "If you are a new applicant, click the button below to start the application process."
            ]

        submit = form.control(name="submit", type="submit", value="new application")

        form = section.form(
            name="returning_applicant",
            legend="Returning applicants:",
            action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="returningApplicant")

        p = form.paragraph()
        p.text = [
            "If you are a returning applicant, please enter your candidate ID",
            "and click the button below to retrieve your application."
            ]

        code = form.text(
            id='cid', name='%s.cid' % self.name, label='candidate ID:'
            )

        submit = form.control(name="submit", type="submit", value="retrieve application")

        return page


    def newApplicant(self, director, page=None):
        # create a record locator
        cid = director.idd.token().locator

        # create an empty Candidate
        from ent.dom.Candidate import Candidate
        candidate = Candidate()
        candidate.id = cid
        candidate.status = 'i'
        director.db.insertRow(candidate)

        # put the candidate record tag in the inventory
        self.inventory.cid = cid

        # put a welcome message up
        page = self._createPage(director, page, candidate)
        content = page._body._content._main
        section = content.document(
            title="Welcome to the OC&amp;C application submission site"
            )
        p = section.paragraph()
        p.text = [
            "Welcome!",
            "Your candidate ID is <b>%s</b>." % candidate.id,
            "Please make a note of it; it is required to gain access to",
            "this site and make changes to the information you have provided."
            ]

        actions = [
            "actor=recruiter",
            "routine=contactInformation",
            "recruiter.cid=%s" % candidate.id
            ]
        target = "%s?%s" % (director.cgihome, "&".join(actions))
        p = section.paragraph()
        p.text = [
            "The easiest way to complete this process is to start with the",
            '<a href="%s">' % target,
            "<b>contact information</b>",
            "</a>",
            "section and walk through all the steps",
            "by clicking <b>submit</b> until the process is complete.",
            "You can revisit any section at any time by selecting from the menu on the left or",
            "by using your browser's <b>back</b> and <b>forward</b> buttons.",
            "Please note that no information is saved unless you click the <b>submit</b>",
            "button at the end of each page."
            ]

        # and draw the first page
        return self.review(director, page)


    def newApplicant(self, director, page=None):
        # put a welcome message up
        page = self._createPage(director, page)
        content = page._body._content._main
        section = content.document(
            title="Welcome to the OC&amp;C application submission site"
            )
        p = section.paragraph()
        p.text = [
            "Welcome!",
            "Please take a few minutes to answer the questions in this and following pages."
            ]

        p = section.paragraph()
        p.text = [
            "Please note that no information is saved unless you click the <b>submit</b>",
            "button at the end of each page."
            ]

        # and draw the first page
        return self.contactInformation(director, page)


    def returningApplicant(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        page = self._createPage(director, page, candidate)
        content = page._body._content._main
        section = content.document(title="Welcome back %s" % candidate.firstname)
        p = section.paragraph()
        p.text = [
            "Your application has been retrieved sucessfully.",
            "You can now navigate through the various pages and make any necessary",
            "corrections and additions.",
            ]

        # draw the first page
        return self.review(director, page)
    

    def review(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        page = self._createPage(director, page, candidate, current="overview")
        content = page._body._content._main

        self._drawReviewPage(director, content, candidate)

        return page


    def contactInformation(self, director, page=None):

        defaults = self.inventory
        candidate = self._locateCandidate(director)

        if candidate:
            defaults.cid = candidate.id
            defaults.firstname = candidate.firstname
            defaults.lastname = candidate.lastname
            defaults.address = candidate.address
            defaults.city = candidate.city
            defaults.state = candidate.state
            defaults.postal = candidate.postal
            defaults.country = candidate.country
            defaults.email = candidate.email
            defaults.phone = candidate.phone

        page = self._createPage(director, page, candidate, current="contact")
        content = page._body._content._main
        self._drawContactInformationPage(director, content, defaults)

        return page


    def preferences(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        record = self.inventory
        record.position = candidate.position
        record.office = candidate.office

        if candidate.startDate.strip():
            startYear, startMonth = candidate.startDate.split('/')
        else:
            startYear = startMonth = ""
            
        record.startYear = startYear.strip()
        record.startMonth = startMonth.strip()

        record.referral = candidate.referral
        
        page = self._createPage(director, page, candidate, current="preferences")
        content = page._body._content._main
        self._drawPreferencesPage(director, content, record)

        return page


    def education(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        record = self.inventory
        record.degree_1 = candidate.degree_1
        record.field_1 = candidate.field_1
        record.school_1 = candidate.school_1
        if candidate.graduation_1.strip():
            gradYear, gradMonth = candidate.graduation_1.split("/")
        else:
            gradYear = gradMonth = ""
        record.graduationYear_1 = gradYear
        record.graduationMonth_1 = gradMonth

        record.degree_2 = candidate.degree_2
        record.field_2 = candidate.field_2
        record.school_2 = candidate.school_2
        if candidate.graduation_2.strip():
            gradYear, gradMonth = candidate.graduation_2.split("/")
        else:
            gradYear = gradMonth = ""
        record.graduationYear_2 = gradYear
        record.graduationMonth_2 = gradMonth

        record.degree_3 = candidate.degree_3
        record.field_3 = candidate.field_3
        record.school_3 = candidate.school_3
        if candidate.graduation_3.strip():
            gradYear, gradMonth = candidate.graduation_3.split("/")
        else:
            gradYear = gradMonth = ""
        record.graduationYear_3 = gradYear
        record.graduationMonth_3 = gradMonth
        
        page = self._createPage(director, page, candidate, current="education")
        content = page._body._content._main
        self._drawEducationPage(director, content, record)

        return page


    def experience(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        record = self.inventory
        record.company_1 = candidate.company_1
        record.position_1 = candidate.position_1
        record.city_1 = candidate.city_1
        record.country_1 = candidate.country_1
        if candidate.start_1.strip():
            startYear, startMonth = candidate.start_1.split("/")
        else:
            startYear = startMonth = ""
        record.startMonth_1 = startMonth
        record.startYear_1 = startYear
        if candidate.end_1.strip():
            endYear, endMonth = candidate.end_1.split("/")
        else:
            endYear = endMonth = ""
        record.endMonth_1 = endMonth
        record.endYear_1 = endYear
        
        record.company_2 = candidate.company_2
        record.position_2 = candidate.position_2
        record.city_2 = candidate.city_2
        record.country_2 = candidate.country_2
        if candidate.start_2.strip():
            startYear, startMonth = candidate.start_2.split("/")
        else:
            startYear = startMonth = ""
        record.startMonth_2 = startMonth
        record.startYear_2 = startYear
        if candidate.end_2.strip():
            endYear, endMonth = candidate.end_2.split("/")
        else:
            endYear = endMonth = ""
        record.endMonth_2 = endMonth
        record.endYear_2 = endYear
        
        record.company_3 = candidate.company_3
        record.position_3 = candidate.position_3
        record.city_3 = candidate.city_3
        record.country_3 = candidate.country_3
        if candidate.start_3.strip():
            startYear, startMonth = candidate.start_3.split("/")
        else:
            startYear = startMonth = ""
        record.startMonth_3 = startMonth
        record.startYear_3 = startYear
        if candidate.end_3.strip():
            endYear, endMonth = candidate.end_3.split("/")
        else:
            endYear = endMonth = ""
        record.endMonth_3 = endMonth
        record.endYear_3 = endYear
        
        page = self._createPage(director, page, candidate, current="work")
        content = page._body._content._main
        self._drawExperiencePage(director, content, record)

        return page


    def resume(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        record = self.inventory

        resume = candidate.resume
        if resume is None:
            resume = ''
        record.resume = resume

        cover = candidate.cover
        if cover is None:
            cover = ''
        record.cover = cover
        
        page = self._createPage(director, page, candidate, current="resume")
        content = page._body._content._main
        self._drawResumePage(director, content, record)

        return page


    def submit(self, director, page=None):
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        links = self._checkCompleteness(director, candidate)
        if not links:
            # do the update
            where = "id='%s'" % candidate.id
            assignments = [
                ("status", "n"),
                ]
            director.db.updateRow(candidate, assignments, where)

        page = self._createPage(director, page, candidate, current="submit")
        content = page._body._content._main

        self._drawSubmitPage(director, content, candidate, links)
        
        return page


    def default(self, director):
        return self.welcome(director)


    def validateContactInformation(self, director):
        errors = {}
        record = self.inventory

        if not record.firstname:
            errors["firstname"] = "This is a required field"
        if not record.lastname:
            errors["lastname"] = "This is a required field"

        if not record.phone:
            errors["phone"] = "This is a required field"
                
        if not record.email:
            errors["email"] = "This is a required field"

        if errors:
            page = director.retrievePage("recruiting")
            content = page._body._content._main
            self._drawContactInformationPage(director, content, record, errors)
            return page

        # ok - no errors
        from ent.dom.Candidate import Candidate
        candidate = self._locateCandidate(director)

        # this must be a new applicant, so let's create a new record
        if not candidate:
            candidate = self._createNewCandidate(director)
            record.cid = candidate.id

        # move the collected data over
        tag = record.cid
        candidate.firstname = record.firstname
        candidate.lastname = record.lastname
        candidate.address = record.address
        candidate.city = record.city
        candidate.state = record.state
        candidate.postal = record.postal
        candidate.country = record.country
        candidate.phone = record.phone
        candidate.email = record.email

        # do the update
        where = "id='%s'" % tag
        assignments = [
            ("firstname", candidate.firstname),
            ("lastname", candidate.lastname),
            ("address", candidate.address),
            ("city", candidate.city),
            ("state", candidate.state),
            ("postal", candidate.postal),
            ("country", candidate.country),
            ("phone", candidate.phone),
            ("email", candidate.email),
            ]
        director.db.updateRow(candidate, assignments, where)

        return self.preferences(director)


    def validatePreferences(self, director):
        record = self.inventory
        tag = record.cid

        # validate
        errors = {}
        if not record.office:
            errors["office"] = "This is a required field and you must make an initial choice"
        if not (record.startYear and record.startMonth):
            errors["startDate"] = "This is a required field and you must make an initial choice"

        if errors:
            page = director.retrievePage("recruiting")
            content = page._body._content._main
            self._drawPreferencesPage(director, content, record, errors)
            return page

        # ok - no errors
        from ent.dom.Candidate import Candidate
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        # move the collected data over
        candidate.position = record.position
        candidate.office = record.office
        candidate.startDate = "%s/%s" % (record.startYear, record.startMonth)
        candidate.referral = record.referral

        # do the update
        where = "id='%s'" % tag
        assignments = [
            ("position", candidate.position),
            ("office", candidate.office),
            ("startDate", candidate.startDate),
            ("referral", candidate.referral),
            ]
        director.db.updateRow(candidate, assignments, where)

        return self.education(director)


    def validateEducation(self, director):
        record = self.inventory
        tag = record.cid

        if not record.degree_1:
            errors["degree_1"] = "You must enter at least one degree"
        if not record.field_1:
            errors["field_1"] = "Please enter your area of concentration"
        if not record.school_1:
            errors["school_1"] = "Please indicate the school you attended"

        if record.degree_2 and not record.field_2:
            errors["field_2"] = "Please enter your area of concentration"
        if record.degree_2 and not record.school_2:
            errors["school_2"] = "Please indicate the school you attended"

        if record.degree_3 and not record.field_3:
            errors["field_3"] = "Please enter your area of concentration"
        if record.degree_3 and not record.school_3:
            errors["school_3"] = "Please indicate the school you attended"

        # ok - no errors 
        from ent.dom.Candidate import Candidate
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        # move the collected data over
        candidate.degree_1 = record.degree_1
        candidate.field_1 = record.field_1
        candidate.school_1 = record.school_1
        if record.graduationYear_1 and record.graduationMonth_1:
            candidate.graduation_1 = "%s/%s" % (record.graduationYear_1, record.graduationMonth_1)
        else:
            candidate.graduation_1 = ""
        
        candidate.degree_2 = record.degree_2
        candidate.field_2 = record.field_2
        candidate.school_2 = record.school_2
        if record.graduationYear_2 and record.graduationMonth_2:
            candidate.graduation_2 = "%s/%s" % (record.graduationYear_2, record.graduationMonth_2)
        else:
            candidate.graduation_2 = ""
        
        candidate.degree_3 = record.degree_3
        candidate.field_3 = record.field_3
        candidate.school_3 = record.school_3
        if record.graduationYear_3 and record.graduationMonth_3:
            candidate.graduation_3 = "%s/%s" % (record.graduationYear_3, record.graduationMonth_3)
        else:
            candidate.graduation_3 = ""

        # do the update
        where = "id='%s'" % tag
        assignments = [
            ("degree_1", candidate.degree_1),
            ("field_1", candidate.field_1),
            ("school_1", candidate.school_1),
            ("graduation_1", candidate.graduation_1),
            ("degree_2", candidate.degree_2),
            ("field_2", candidate.field_2),
            ("school_2", candidate.school_2),
            ("graduation_2", candidate.graduation_2),
            ("degree_3", candidate.degree_3),
            ("field_3", candidate.field_3),
            ("school_3", candidate.school_3),
            ("graduation_3", candidate.graduation_3),
            ]
        director.db.updateRow(candidate, assignments, where)

        return self.experience(director)


    def validateExperience(self, director):
        record = self.inventory
        tag = record.cid

        # ok - no errors 
        from ent.dom.Candidate import Candidate
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        # move the collected data over
        candidate.company_1 = record.company_1
        candidate.position_1 = record.position_1
        candidate.city_1 = record.city_1
        candidate.country_1 = record.country_1
        if record.startYear_1 and record.startMonth_1:
            candidate.start_1 = "%s/%s" % (record.startYear_1, record.startMonth_1)
        else:
            candidate.start_1 = ""
        if record.endYear_1 and record.endMonth_1:
            candidate.end_1 = "%s/%s" % (record.endYear_1, record.endMonth_1)
        else:
            candidate.end_1 = ""
        
        candidate.company_2 = record.company_2
        candidate.position_2 = record.position_2
        candidate.city_2 = record.city_2
        candidate.country_2 = record.country_2
        if record.startYear_2 and record.startMonth_2:
            candidate.start_2 = "%s/%s" % (record.startYear_2, record.startMonth_2)
        else:
            candidate.start_2 = ""
        if record.endYear_2 and record.endMonth_2:
            candidate.end_2 = "%s/%s" % (record.endYear_2, record.endMonth_2)
        else:
            candidate.end_2 = ""
        
        candidate.company_3 = record.company_3
        candidate.position_3 = record.position_3
        candidate.city_3 = record.city_3
        candidate.country_3 = record.country_3
        if record.startYear_3 and record.startMonth_3:
            candidate.start_3 = "%s/%s" % (record.startYear_3, record.startMonth_3)
        else:
            candidate.start_3 = ""
        if record.endYear_3 and record.endMonth_3:
            candidate.end_3 = "%s/%s" % (record.endYear_3, record.endMonth_3)
        else:
            candidate.end_3 = ""
        
        # do the update
        where = "id='%s'" % tag
        assignments = [
            ("company_1", candidate.company_1),
            ("position_1", candidate.position_1),
            ("city_1", candidate.city_1),
            ("country_1", candidate.country_1),
            ("start_1", candidate.start_1),
            ("end_1", candidate.end_1),
            
            ("company_2", candidate.company_2),
            ("position_2", candidate.position_2),
            ("city_2", candidate.city_2),
            ("country_2", candidate.country_2),
            ("start_2", candidate.start_2),
            ("end_2", candidate.end_2),
        
            ("company_3", candidate.company_3),
            ("position_3", candidate.position_3),
            ("city_3", candidate.city_3),
            ("country_3", candidate.country_3),
            ("start_3", candidate.start_3),
            ("end_3", candidate.end_3),
            ]
        director.db.updateRow(candidate, assignments, where)

        return self.resume(director)


    def validateResume(self, director):
        record = self.inventory
        tag = record.cid

        if not record.cover:
            errors['cover'] = "Please paste your cover letter in this box"
        if not record.resume:
            errors['cover'] = "Please paste your resume in this box"
            
        # ok - no errors 
        from ent.dom.Candidate import Candidate
        candidate = self._locateCandidate(director)
        if not candidate:
            return self._postErrorNotification(director)

        # do the update
        where = "id='%s'" % tag
        assignments = [
            ("cover", record.cover),
            ("resume", record.resume),
            ]
        director.db.updateRow(candidate, assignments, where)

        return self.review(director)


    def __init__(self, name=None):
        if name is None:
            name = "recruiter"
        super(Recruiter, self).__init__(name)
        return


    def _drawReviewPage(self, director, content, candidate):
        section = content.document(
            title="Online Application Status"
            )

        p = section.paragraph()
        p.text = [
            "Use this page to keep track of your progress in the application submission process.",
            "It is reachable any time through the menu entry marked <b>overview</b> in the",
            "navigational panel on the left.",
            ]

        p = section.paragraph()
        p.text = [
            "Your candidate ID is <b>%s</b>." % candidate.id,
            ]

        p = section.paragraph()
        links = self._checkCompleteness(director, candidate)
        if links:
            p.text = [
                "You must complete the following sections before",
                "you can submit your application:",
                ", ".join(links)
                ]
        else:
            actions = [
                "actor=recruiter",
                "routine=submit",
                "recruiter.cid=%s" % candidate.id
                ]
            target = "%s?%s" % (director.cgihome, "&".join(actions))
            p.text = [
                'You have completed all the required steps.',
                'If you are done making changes, click the',
                '<b><a href="%s">submit application</a></b>' % target,
                'button on the menu.'
                ]

        p = section.paragraph()
        p.text = [
            "Here is a summary of the information you have provided so far:"
            ]

        # contact information
        section = content.document(
            title="Contact Information"
            )
        
        p = section.literal()
        if candidate.firstname:
            name = "%s %s" % (candidate.firstname, candidate.lastname)
            address = "%s, %s %s %s, %s" % (
                candidate.address, candidate.city, candidate.state, candidate.postal,
                candidate.country
                )
            p.text = [
                "<p>",
                "<table>",

                "<tr>",
                "<td><em>Name:</em></td>",
                "<td><b>%s</b></td>" % name,
                "</tr>",

                "<tr>",
                "<td><em>Address:</em></td>",
                "<td><b>%s</b></td>" % address,
                "</tr>",

                "<tr>",
                "<td><em>Telephone:</em></td>",
                "<td><b>%s</b></td>" % candidate.phone,
                "</tr>",

                "<tr>",
                "<td><em>Email:</em></td>",
                "<td><b>%s</b></td>" % candidate.email,
                "</tr>",

                "</table>",
                "</p>",
                ]
        else:
            p.text = [
                "No contact information has been supplied yet."
                ]

        form = section.form(name="contact_info", action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="contactInformation")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.id)
        
        # add the submit button
        submit = form.submitButton(value="edit")

        # position
        section = content.document(
            title="Preferences"
            )
        
        if candidate.firstname:
            p = section.literal()
            p.text = [
                "<p>",
                "<table>",

                "<tr>",
                "<td><em>Position:</em></td>",
                "<td><b>%s</b></td>" % candidate.position,
                "</tr>",

                "<tr>",
                "<td><em>Office:</em></td>",
                "<td><b>%s</b></td>" % candidate.office,
                "</tr>",

                "<tr>",
                "<td><em>Available:</em></td>",
                "<td><b>%s</b></td>" % candidate.startDate,
                "</tr>",

                "<tr>",
                "<td><em>Referral:</em></td>",
                "<td><b>%s</b></td>" % candidate.referral,
                "</tr>",

                "</table>",
                "</p>",
                ]
        else:
            p = section.paragraph()
            p.text = [
                "You have not indicated your position preferences yet."
                ]

        form = section.form(name="preferences", action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="preferences")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.id)
        
        # add the submit button
        submit = form.submitButton(value="edit")

        # education
        section = content.document(
            title="Education"
            )
        
        p = section.literal()
        p.text = [
            "<p>",
            "<table>",
            ]

        if candidate.degree_1:
            degree = ", ".join([
                candidate.degree_1, candidate.field_1, candidate.school_1, candidate.graduation_1
                ])
            p.text += [
                "<tr>",
                "<td>1.</td>"
                "<td><b>%s</b></td>" % degree,
                "</tr>",
                ]

        if candidate.degree_2:
            degree = ", ".join([
                candidate.degree_2, candidate.field_2, candidate.school_2, candidate.graduation_2
                ])
            p.text += [
                "<tr>",
                "<td>2.</td>"
                "<td><b>%s</b></td>" % degree,
                "</tr>",
                ]

        if candidate.degree_3:
            degree = ", ".join([
                candidate.degree_3, candidate.field_3, candidate.school_3, candidate.graduation_3
                ])
            p.text += [
                "<tr>",
                "<td>3.</td>"
                "<td><b>%s</b></td>" % degree,
                "</tr>",
                ]

        if not (candidate.degree_1 or candidate.degree_2 or candidate.degree_3):
            p = section.paragraph()
            p.text = [
                "<tr>",
                "<td>No education information has been supplied.</td>"
                "</tr>",
                "<tr>",
                ]
        
        p.text += [
            "</table>",
            "</p>"
            ]

        # add the submit button
        form = section.form(name="education", action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="education")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.id)
        
        submit = form.submitButton(value="edit")

        # work experience
        section = content.document(
            title="Work experience"
            )

        p = section.literal()
        p.text = [
            "<p>",
            "<table>",
            ]

        if candidate.company_1:
            position = ", ".join([
                candidate.position_1, candidate.company_1,
                candidate.city_1, candidate.country_1,
                ])
            start = candidate.start_1
            if candidate.end_1:
                end = candidate.end_1
            else:
                end = "present"
            p.text += [
                "<tr>",
                "<td>1.</td>"
                "<td><b>%s</b></td>" % position,
                "</tr>",
                "<tr>",
                "<td></td>",
                "<td>From <b>%s</b> to <b>%s</b></td>" % (start, end),
                "</tr>",
                ]

        if candidate.company_2:
            position = ", ".join([
                candidate.position_2, candidate.company_2,
                candidate.city_2, candidate.country_2,
                ])
            start = candidate.start_2
            end = candidate.end_2
            p.text += [
                "<tr>",
                "<td>2.</td>"
                "<td><b>%s</b></td>" % position,
                "</tr>",
                "<tr>",
                "<td></td>",
                "<td>From <b>%s</b> to <b>%s</b></td>" % (start, end),
                "</tr>",
                ]

        if candidate.company_3:
            position = ", ".join([
                candidate.position_3, candidate.company_3,
                candidate.city_3, candidate.country_3,
                ])
            start = candidate.start_3
            end = candidate.end_3
            p.text += [
                "<tr>",
                "<td>3.</td>"
                "<td><b>%s</b></td>" % position,
                "</tr>",
                "<tr>",
                "<td></td>",
                "<td>From <b>%s</b> to <b>%s</b></td>" % (start, end),
                "</tr>",
                ]
        if not (candidate.company_1 or candidate.company_2 or candidate.company_3):
            p = section.paragraph()
            p.text = [
                "<tr>",
                "<td>No work experience information has been supplied.</td>"
                "</tr>",
                "<tr>",
                ]
        
        p.text += [
            "</table>",
            "</p>"
            ]

        form = section.form(
            name="experience",
            action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="experience")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.id)
        
        # add the submit button
        submit = form.submitButton(value="edit")

        # resume
        section = content.document(
            title="Cover letter and resume"
            )

        if candidate.cover:
            cover = "<b>HAVE</b>"
        else:
            cover = "<b>HAVE NOT</b>"
        p = section.paragraph()
        p.text = [
            "You %s uploaded a cover letter" % cover
            ]
        
        if candidate.resume:
            resume = "<b>HAVE</b>"
        else:
            resume = "<b>HAVE NOT</b>"
        p = section.paragraph()
        p.text = [
            "You %s uploaded your resume" % resume
            ]

        form = section.form(
            name="cover",
            action=director.cgihome)
        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="resume")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.id)
        
        # add the submit button
        submit = form.submitButton(value="edit")


        return
    

    def _drawContactInformationPage(self, director, content, candidate, errors=None):
        section = content.document(
            title="Step 1: Contact Information"
            )

        if errors:
            p = section.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the values you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the data form
        import ent.content
        form = section.form(name='recruiting_contactinfo', action=director.cgihome)

        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="validateContactInformation")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.cid)

        box = form.box()

        if candidate.firstname:
            text = candidate.firstname
        else:
            text = ""
        firstname = box.text(
            required=True,
            id='firstname', name='%s.firstname' % self.name, label='First name:',
            value=text
            )
        #firstname.help = "Please enter your given name"
        if "firstname" in errors:
            firstname.error = errors["firstname"]

        if candidate.lastname:
            text = candidate.lastname
        else:
            text = ""
        lastname = box.text(
            required=True,
            id='lastname', name='%s.lastname' % self.name, label='Last name:',
            value=text
            )
        #lastname.help = "Please enter your family name"
        if "lastname" in errors:
            lastname.error = errors["lastname"]

        if candidate.email:
            text = candidate.email
        else:
            text = ""
        email = form.text(
            required=True,
            id='email', name='%s.email' % self.name, label='Email:',
            value=text
            )
        email.help = " ".join([
            "Please enter an email address where we can contact you concerning this application.",
            "It is important to double check that you have entered the address correctly",
            "because email is the primary means of communication with our candidates."
            ])
        if "email" in errors:
            email.error = errors["email"]

        # address information
        if candidate.address:
            text = candidate.address
        else:
            text = ""
        address = form.text(
            id='address', name='%s.address' % self.name, label='Address:',
            value=text
            )
        address.help = "Please enter your street address"
        if "address" in errors:
            address.error = errors["address"]


        box = form.box()
        if candidate.city:
            text = candidate.city
        else:
            text = ""
        city = box.text(
            id='city', name='%s.city' % self.name, label='City:',
            value=text
            )
        #city.help = "Please enter your city"
        if "city" in errors:
            city.error = errors["city"]

        if candidate.state:
            text = candidate.state
        else:
            text = ""
        state = box.text(
            id='state', name='%s.state' % self.name, label='State/Province:',
            value=text
            )
        #state.help = "Please enter your state or province"
        if "state" in errors:
            state.error = errors["state"]

        if candidate.postal:
            text = candidate.postal
        else:
            text = ""
        postal = box.text(
            id='postal', name='%s.postal' % self.name, label='Zip/Postal code:',
            value=text
            )
        #postal.help = "Please enter your zip code or postal code"
        if "postal" in errors:
            postal.error = errors["postal"]

        if candidate.country:
            text = candidate.country
        else:
            text = ""
        country = box.text(
            id='country', name='%s.country' % self.name, label='Country:',
            value=text
            )
        #country.help = "Please enter your country"
        if "country" in errors:
            country.error = errors["country"]

        if candidate.phone:
            text = candidate.phone
        else:
            text = ""
        phone = form.text(
            required=True,
            id='phone', name='%s.phone' % self.name, label='Telephone:',
            value=text
            )
        phone.help = " ".join([
            "Please enter a phone number where you can be reached during business hours",
            "If you live outside the US, please don't forget to include your country code."
            ])
        if "phone" in errors:
            phone.error = errors["phone"]

        # add the submit button
        submit = form.submitButton(value="save")

        return


    def _drawPreferencesPage(self, director, content, candidate, errors=None):

        locations = director.clerk.indexLocations()
        
        section = content.document(
            title="Step 2: Preferences"
            )

        if errors:
            p = section.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the values you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the data form
        import ent.content
        form = section.form(name='recruiting_preferences', action=director.cgihome)

        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="validatePreferences")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.cid)
        email = form.hidden(name='%s.email' % self.name, value=candidate.email)

        if candidate.position:
            selection = candidate.position
        else:
            selection = None
        positionSelector = ent.content.titleSelector(
            id="position", name="%s.position" % self.name,
            label="Position:", selected=selection)
        positionSelector.help = 'Please indicate the level at which you envision joining the company'
        form.field(control=positionSelector, required=True)
        if "position" in errors:
            positionSelector.error = errors["position"]

        if candidate.office:
            selection = candidate.office
        else:
            selection = None
        officeSelector = ent.content.locationSelector(
            locations=locations,
            id="office", name="%s.office" % self.name,
            label="Preferred office:", selected=selection)
        officeSelector.help = " ".join([
            'Please indicate your initial preference.',
            'All candidates are considered by all offices, so you are not',
            'limiting your opportunities by making a selection.',
            'If you are invited for an interview, you will be able to discuss',
            'other locations of interest to you.'
            ])
        form.field(control=officeSelector, required=True)
        if "office" in errors:
            officeSelector.error = errors["office"]

        # create the date picker
        datePick = form.box(
            required=True,
            id="startDate", label='Start date:',
            )
        datePick.help = "When are you available to start work?"
        if "startDate" in errors:
            datePick.error = errors["startDate"]

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.startMonth" % self.name,
            label="",
            selected=candidate.startMonth)
        datePick.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2007, last=2009,
            id="startYear", name="%s.startYear" % self.name,
            label="",
            selected=candidate.startYear)
        datePick.add(yearSelector)


        if candidate.referral:
            selection = candidate.referral
        else:
            selection = None
        referralSelector = ent.content.referrerSelector(
            id="referral", name="%s.referral" % self.name,
            label="Referral:", selected=selection)
        referralSelector.help = "How did you hear about positions with OC&amp;C?"
        form.field(control=referralSelector, required=True)
        if "referral" in errors:
            referralSelector.error = errors["referral"]

        # add the submit button
        submit = form.submitButton(value="save")

        return


    def _drawEducationPage(self, director, content, candidate, errors=None):
        import ent.content

        # start the document
        section = content.document(
            title="Step 3: Education"
            )

        if errors:
            p = section.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the values you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the data form
        import ent.content
        form = section.form(name='recruiting_education', action=director.cgihome)

        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="validateEducation")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.cid)
        email = form.hidden(name='%s.email' % self.name, value=candidate.email)

        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate the most recent degree you hold or working towards."
            ]

        box = form.box()

        if candidate.degree_1:
            selection = candidate.degree_1
        else:
            selection = None
        degree_1Selector = ent.content.degreeSelector(
            id='degree_1', name='%s.degree_1' % self.name,
            label="Degree:", selected=selection)
        degree_1Selector.help = "Please pick one from the list"
        box.field(control=degree_1Selector, required=True)
        if "degree_1" in errors:
            degree_1Selector.error = errors["degree_1"]

        if candidate.field_1 is None:
            value = ""
        else:
            value = candidate.field_1
        field_1 = box.text(
            required=True,
            id='field_1', name='%s.field_1' % self.name, label='Major/Field:',
            value=value
            )
        field_1.help = "Please specify the area of concentration"
        if "field_1" in errors:
            field_1.error = errors["field_1"]

        if candidate.school_1 is None:
            value = ""
        else:
            value = candidate.school_1
        school_1 = box.text(
            required=True,
            id='school_1', name='%s.school_1' % self.name, label='University:',
            value=value
            )
        school_1.help = "Please specify the granting institution"
        if "school_1" in errors:
            school_1.error = errors["school_1"]

        # create the date picker
        graduation_1 = form.box(
            required=True,
            id='graduation_1', label='Graduation date:',
            )
        graduation_1.help = "Please specify the graduation month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.graduationMonth_1" % self.name,
            label="",
            selected=candidate.graduationMonth_1)
        graduation_1.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.graduationYear_1" % self.name,
            label="",
            selected=candidate.graduationYear_1)
        graduation_1.add(yearSelector)

        # earlier degree
        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate an earlier degree you hold."
            ]

        box = form.box()

        if candidate.degree_2:
            selection = candidate.degree_2
        else:
            selection = None
        degree_2Selector = ent.content.degreeSelector(
            id='degree_2', name='%s.degree_2' % self.name,
            label="Degree:", selected=selection)
        degree_2Selector.help = "Please pick one from the list"
        box.field(control=degree_2Selector)
        if "degree_2" in errors:
            degree_2Selector.error = errors["degree_2"]

        if candidate.field_2 is None:
            value = ""
        else:
            value = candidate.field_2
        field_2 = box.text(
            id='field_2', name='%s.field_2' % self.name, label='Major/Field:',
            value=value
            )
        field_2.help = "Please specify the area of concentration"
        if "field_2" in errors:
            field_2.error = errors["field_2"]

        if candidate.school_2 is None:
            value = ""
        else:
            value = candidate.school_2
        school_2 = box.text(
            id='school_2', name='%s.school_2' % self.name, label='University:',
            value=value
            )
        school_2.help = "Please specify the institution that granted this degree"
        if "school_2" in errors:
            school_2.error = errors["school_2"]

        # create the date picker
        graduation_2 = form.box(
            id='graduation_2', label='Graduation date:',
            )
        graduation_2.help = "Please specify the graduation month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.graduationMonth_2" % self.name,
            label="",
            selected=candidate.graduationMonth_2)
        graduation_2.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.graduationYear_2" % self.name,
            label="",
            selected=candidate.graduationYear_2)
        graduation_2.add(yearSelector)

        # earlier degree
        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate an earlier degree you hold."
            ]

        box = form.box()

        if candidate.degree_3:
            selection = candidate.degree_3
        else:
            selection = None
        degree_3Selector = ent.content.degreeSelector(
            id='degree_3', name='%s.degree_3' % self.name,
            label="Degree:", selected=selection)
        degree_3Selector.help = "Please pick one from the list"
        box.field(control=degree_3Selector)
        if "degree_3" in errors:
            degree_3Selector.error = errors["degree_3"]

        if candidate.field_3 is None:
            value = ""
        else:
            value = candidate.field_3
        field_3 = box.text(
            id='field_3', name='%s.field_3' % self.name, label='Major/Field:',
            value=value
            )
        field_3.help = "Please specify the area of concentration"
        if "field_3" in errors:
            field_3.error = errors["field_3"]

        if candidate.school_3 is None:
            value = ""
        else:
            value = candidate.school_3
        school_3 = box.text(
            id='school_3', name='%s.school_3' % self.name, label='University:',
            value=value
            )
        school_3.help = "Please specify the granting institution"
        if "school_3" in errors:
            school_3.error = errors["school_3"]

        # create the date picker
        graduation_3 = form.box(
            id='graduation_3', label='Graduation date:'
            )
        graduation_3.help = "Please specify the graduation month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.graduationMonth_3" % self.name,
            label="",
            selected=candidate.graduationMonth_3)
        graduation_3.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.graduationYear_3" % self.name,
            label="",
            selected=candidate.graduationYear_3)
        graduation_3.add(yearSelector)

        # add the submit button
        submit = form.submitButton(value="save")

        return


    def _drawExperiencePage(self, director, content, candidate, errors=None):
        import ent.content

        # start the document
        section = content.document(
            title="Step 4: Work Experience"
            )

        if errors:
            p = section.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the values you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the data form
        import ent.content
        form = section.form(name='recruiting_experience', action=director.cgihome)

        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="validateExperience")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.cid)
        email = form.hidden(name='%s.email' % self.name, value=candidate.email)

        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate your most recent position"
            ]

        box = form.box()

        if candidate.company_1 is None:
            value = ""
        else:
            value = candidate.company_1
        company_1 = box.text(
            id='company_1', name='%s.company_1' % self.name, label='Company:',
            value=value
            )
        #company_1.help = "Please specify your employer"
        if "company_1" in errors:
            company_1.error = errors["company_1"]

        if candidate.position_1 is None:
            value = ""
        else:
            value = candidate.position_1
        position_1 = box.text(
            id='position_1', name='%s.position_1' % self.name, label='Position:',
            value=value
            )
        #position_1.help = "Please specify the position you held"
        if "position_1" in errors:
            position_1.error = errors["position_1"]

        box.newline()

        if candidate.city_1 is None:
            value = ""
        else:
            value = candidate.city_1
        city_1 = box.text(
            id='city_1', name='%s.city_1' % self.name, label='City:',
            value=value
            )
        #city_1.help = "Please specify the employment location"
        if "city_1" in errors:
            city_1.error = errors["city_1"]

        if candidate.country_1 is None:
            value = ""
        else:
            value = candidate.country_1
        country_1 = box.text(
            id='country_1', name='%s.country_1' % self.name, label='Country:',
            value=value
            )
        #country_1.help = "Please specify the state or province"
        if "country_1" in errors:
            country_1.error = errors["country_1"]

        # create the date picker
        start_1 = form.box(
            id='start_1', label='Start date:',
            )
        start_1.help = "Please specify the start month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.startMonth_1" % self.name,
            label="",
            selected=candidate.startMonth_1)
        start_1.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.startYear_1" % self.name,
            label="",
            selected=candidate.startYear_1)
        start_1.add(yearSelector)

        end_1 = form.box(
            id='end_1', label='End date:',
            )
        end_1.help = " ".join([
            "Please specify the end month and year.",
            "If you are still working there, just leave blank"
            ])

        monthSelector = ent.content.monthSelector(
            id="endMonth", name="%s.endMonth_1" % self.name,
            label="",
            selected=candidate.endMonth_1)
        end_1.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="endYear", name="%s.endYear_1" % self.name,
            label="",
            selected=candidate.endYear_1)
        end_1.add(yearSelector)

        # earlier
        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate an earlier position"
            ]

        box = form.box()

        if candidate.company_2 is None:
            value = ""
        else:
            value = candidate.company_2
        company_2 = box.text(
            id='company_2', name='%s.company_2' % self.name, label='Company:',
            value=value
            )
        #company_2.help = "Please specify your employer"
        if "company_2" in errors:
            company_2.error = errors["company_2"]

        if candidate.position_2 is None:
            value = ""
        else:
            value = candidate.position_2
        position_2 = box.text(
            id='position_2', name='%s.position_2' % self.name, label='Position:',
            value=value
            )
        #position_2.help = "Please specify the position you held"
        if "position_2" in errors:
            position_2.error = errors["position_2"]

        box.newline()

        if candidate.city_2 is None:
            value = ""
        else:
            value = candidate.city_2
        city_2 = box.text(
            id='city_2', name='%s.city_2' % self.name, label='City:',
            value=value
            )
        #city_2.help = "Please specify the employment location"
        if "city_2" in errors:
            city_2.error = errors["city_2"]

        if candidate.country_2 is None:
            value = ""
        else:
            value = candidate.country_2
        country_2 = box.text(
            id='country_2', name='%s.country_2' % self.name, label='Country:',
            value=value
            )
        #country_2.help = "Please specify the country"
        if "country_2" in errors:
            country_2.error = errors["country_2"]

        # create the date picker
        start_2 = form.box(
            id='start_2', label='Start date:',
            )
        start_2.help = "Please specify the start month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.startMonth_2" % self.name,
            label="",
            selected=candidate.startMonth_2)
        start_2.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.startYear_2" % self.name,
            label="",
            selected=candidate.startYear_2)
        start_2.add(yearSelector)

        end_2 = form.box(
            id='end_2', label='End date:',
            )
        end_2.help = "Please specify the end month and year"

        monthSelector = ent.content.monthSelector(
            id="endMonth", name="%s.endMonth_2" % self.name,
            label="",
            selected=candidate.endMonth_2)
        end_2.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="endYear", name="%s.endYear_2" % self.name,
            label="",
            selected=candidate.endYear_2)
        end_2.add(yearSelector)

        # earlier
        p = form.paragraph(cls="success")
        p.text = [
            "Please indicate an earlier position"
            ]

        box = form.box()

        if candidate.company_3 is None:
            value = ""
        else:
            value = candidate.company_3
        company_3 = box.text(
            id='company_3', name='%s.company_3' % self.name, label='Company:',
            value=value
            )
        #company_3.help = "Please specify your employer"
        if "company_3" in errors:
            company_3.error = errors["company_3"]

        if candidate.position_3 is None:
            value = ""
        else:
            value = candidate.position_3
        position_3 = box.text(
            id='position_3', name='%s.position_3' % self.name, label='Position:',
            value=value
            )
        #position_3.help = "Please specify the position you held"
        if "position_3" in errors:
            position_3.error = errors["position_3"]

        box.newline()
        
        if candidate.city_3 is None:
            value = ""
        else:
            value = candidate.city_3
        city_3 = box.text(
            id='city_3', name='%s.city_3' % self.name, label='City:',
            value=value
            )
        #city_3.help = "Please specify the employment location"
        if "city_3" in errors:
            city_3.error = errors["city_3"]

        if candidate.country_3 is None:
            value = ""
        else:
            value = candidate.country_3
        country_3 = box.text(
            id='country_3', name='%s.country_3' % self.name, label='Country:',
            value=value
            )
        #country_3.help = "Please specify the country"
        if "country_3" in errors:
            country_3.error = errors["country_3"]

        # create the date picker
        start_3 = form.box(
            id='start_3', label='Start date:',
            )
        start_3.help = "Please specify the start month and year"

        monthSelector = ent.content.monthSelector(
            id="startMonth", name="%s.startMonth_3" % self.name,
            label="",
            selected=candidate.startMonth_3)
        start_3.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="startYear", name="%s.startYear_3" % self.name,
            label="",
            selected=candidate.startYear_3)
        start_3.add(yearSelector)

        end_3 = form.box(
            id='end_3', label='End date:',
            )
        end_3.help = "Please specify the end month and year"

        monthSelector = ent.content.monthSelector(
            id="endMonth", name="%s.endMonth_3" % self.name,
            label="",
            selected=candidate.endMonth_3)
        end_3.add(monthSelector)

        yearSelector = ent.content.yearSelector(
            first=2009, last=1960,
            id="endYear", name="%s.endYear_3" % self.name,
            label="",
            selected=candidate.endYear_3)
        end_3.add(yearSelector)

        # add the submit button
        submit = form.submitButton(value="save")

        return


    def _drawResumePage(self, director, content, candidate, errors=None):
        import ent.content

        # start the document
        section = content.document(
            title="Step 5: Cover letter and resume"
            )

        if errors:
            p = section.paragraph(cls="error")
            p.text = [
                "The form you filled out contained some errors.",
                "Please look through the values you have entered and correct any mistakes"
                ]
        else:
            errors={}

        # build the data form
        form = section.form(name='recruiting_resume', action=director.cgihome)

        targetActor = form.hidden(name='actor', value=self.name)
        targetRoutine = form.hidden(name='routine', value="validateResume")
        cid = form.hidden(name='%s.cid' % self.name, value=candidate.cid)
        email = form.hidden(name='%s.email' % self.name, value=candidate.email)

        cover = form.textarea(
            required=True,
            id='cover', name='%s.cover' % self.name, label='Cover letter:',
            cols='80', rows='10', wrap='soft',
            default=candidate.cover
            )
        cover.help = " ".join([
            "Please cut and paste a text-only version of your cover letter.",
            "Do not worry about formatting, as long as the layout is readable."
            "Try to limit yourself to 10,000 characters."
            ])

        resume = form.textarea(
            required=True,
            id='resume', name='%s.resume' % self.name, label='Resume:',
            cols='80', rows='10', wrap='soft',
            default=candidate.resume
            )
        resume.help = " ".join([
            "Please cut and paste a text-only version of your resume.",
            "Again, do not worry about formatting, as long as the layout is readable."
            "Try to limit yourself to 10,000 characters."
            ])

        # add the submit button
        submit = form.submitButton(value="save")

        return


    def _drawSubmitPage(self, director, content, candidate, links):
        section = content.document(
            title="Application Submission"
            )
        
        if not links:
            p = section.paragraph(cls="success")
            p.text = [
                "You have completed the online application submission process."
                ]

            p = section.paragraph()
            p.text = [
                "Thank you for your interest in OC&amp;C Strategy Consultants.",
                "A member of our recruiting team will be reviewing your application",
                "over the coming weeks.",
                "We'll be in touch if there appears to be a good fit given our",
                "short and long term needs."
                ]
            p = section.paragraph()
            p.text = [
                "In the meantime, you can learn more about OC&amp;C on our",
                '<a href="www.occstrategy.com">website</a>,',
                "where you can find dates for our upcoming on-campus recruiting events."
                ]
            p = section.paragraph()
            p.text = [
                "Warm regards,"
                ]

            p = section.paragraph()
            p.text = [
                "<em>The OC&amp;C Recruiting Team</em>"
                ]
            return

        p = section.paragraph(cls="error")
        p.text = [
            "You must complete the following sections before",
            "you can submit your application:",
            ", ".join(links)
            ]

        p = section.paragraph()
        p.text = [
            "Please provide the missing information and submit your application again."
            ]
        return


    def _locateCandidate(self, director, cid=None, strict=False):
        from ent.dom.Candidate import Candidate

        if cid is None:
            cid = self.inventory.cid.upper()
        if not cid:
            return None

        candidates = director.db.fetchall(Candidate, where="id='%s'" % cid)
        if not candidates:
            return None

        candidate = candidates[0]
        if not strict:
            return candidate
            
        email = self.inventory.email
        if candidate.email != email:
            return None

        return candidate


    def _createPage(self, director, page, candidate=None, current=None):
        if not page:
            page = director.retrievePage("recruiting")

        # add the navigation menu
        if candidate:
            left = page._body._content.leftColumn()
            portlet = director.retrievePortlet("recruiting")
            if portlet:
                portlet.createEntries(candidate.id, current)
                left.add(portlet)

        return page


    def _postErrorNotification(self, director):
        page = director.retrievePage("recruiting")
        content = page._body._content._main
        section = content.document(title="Error")
        p = section.paragraph(cls="error")
        p.text = [
            "This application could not be located. Please",
            '<a href="%s?actor=recruiter">try</a> again.' % director.cgihome
            ]
        return page


    def _checkCompleteness(self, director, candidate):
        missing = []
        if not candidate.firstname:
            missing.append(("contact&nbsp;information", "contactInformation"))
        if not candidate.position:
            missing.append(("preferences", "preferences"))
        if not candidate.degree_1:
            missing.append(("education", "education"))
        if not candidate.company_1:
            missing.append(("work&nbsp;experience", "experience"))
        if not candidate.cover or not candidate.resume:
            missing.append(("cover&nbsp;letter&nbsp;and&nbsp;resume", "resume"))

        links = []
        actions = [
            "actor=recruiter",
            "routine=%s",
            "recruiter.cid=%s" % candidate.id
            ]
        target = "%s?%s" % (director.cgihome, "&".join(actions))
        for text, routine in missing:
            href = target % routine
            links.append('<a href="%s"><b>%s</b></a>' % (href, text))

        return links


    def _createNewCandidate(self, director):
        # create a record locator
        cid = director.idd.token().locator

        # create an empty Candidate
        from ent.dom.Candidate import Candidate
        candidate = Candidate()
        candidate.id = cid

        # fill out the fields we need for the email
        candidate.email = self.inventory.email
        candidate.firstname = self.inventory.firstname
        candidate.status = 'i'

        # save in the database
        director.db.insertRow(candidate)

        # send an email with the candidate ID
        # get the message template
        announcement = director.retrieveComponent(
            "new-candidate",
            factory="announcement", args=[director, candidate],
            vault=['announcements'])

        import ent.components

        # create the postman
        postman = ent.components.postman()
        self.configureComponent(postman)
        postman.init()

        # create the announcer
        announcer = ent.components.announcer()
        self.configureComponent(announcer)
        announcer.init()

        # send the email
        announcement.announce(director, announcer=announcer, postman=postman)

        return candidate

    
# version
__id__ = "$Id: Recruiter.py,v 1.31 2008-04-14 05:06:15 aivazis Exp $"

# End of file 
