# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from luban.content import load
from luban.content.Link import Link

def settingsLink(director, id):
    """Displays settings of the simulation"""
    settings  = director.clerk.getQESettings(where="simulationid='%s'" % id )

    # Default link
    link = Link(label="Create",
                Class="epsc-action-create",
                tip     = "Set simulation environment",
                onclick=load(actor      = "material_simulations/epsc/settings-add",
                             id         = id)
                )

    if settings:
        s = settings[0]
        if s:
            link = Link(label   = s.sname,
                        Class="action-link",
                        onclick = load(actor    = "material_simulations/epsc/settings-view",
                                     id         = id,
                                     configid   = s.id)
                        )

    return link



def serverLink(director, id):
    "Returns server link"
    server = None
    link = "None"

    settings    = director.clerk.getQESettings(where="simulationid='%s'" % id )
    if not settings:# or not settings[0]:
        return link

    setting     = settings[0]
    server = director.clerk.getServers(id = setting.serverid )

    if not server:
        return link


    link = Link(label   = server.address,
                Class   = "action-link",
                tip     = "Show details of computational cluster",
                onclick = select(id='').append(load(actor='server/load', routine='createDialog'))
                )

    return link


__date__ = "$Mar 23, 2011 7:15:15 PM$"


