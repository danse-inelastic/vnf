from AbstractNeutronComponent import AbstractNeutronComponent as base, NeutronComponentTableBase as TableBase


class Monitor(base):

    category = 'monitors'
    
    pass # end of Monitor




class MonitorTableBase(TableBase):

    category = Monitor.category

    pass # end of MonitorTableBase
