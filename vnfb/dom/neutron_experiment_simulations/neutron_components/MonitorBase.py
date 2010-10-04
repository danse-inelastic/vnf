from AbstractNeutronComponent import AbstractNeutronComponent as base, NeutronComponentTableBase as TableBase


class MonitorBase(base):

    category = 'monitors'
    
    pass # end of Monitor




class MonitorTableBase(TableBase):

    category = MonitorBase.category

    pass # end of MonitorTableBase
