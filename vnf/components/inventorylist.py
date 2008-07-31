# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import action_link, actionRequireAuthentication


def list( container, document, actor, director,
          routines = ['edit'] ):
    p = document.paragraph()

    formatstr = '%(index)s: %(name)s '
    formatstr += ' '.join(
        [ '(%'+'(%slink)s)' % routine for routine in routines ]
        )

    for i, element in enumerate( container ):
        
        p = document.paragraph()

        subs = {'name': element.short_description,
                'index': i+1}
        
        #links
        for routine in routines:
            link = action_link(
                actionRequireAuthentication(
                actor, director.sentry,
                routine = routine,
                label = routine,
                id = element.id,
                ),  director.cgihome
                )
            subs[ '%slink' % routine ] = link
            continue

        p.text += [
            formatstr % subs,
            ]
        continue
    return


# version
__id__ = "$Id$"

# End of file 
