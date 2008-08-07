
def tables():
    ret = []

    from _referenceset import _ReferenceTable
    ret.append( _ReferenceTable )
    
    from _geometer import PositionOrientationRegistry
    ret.append( PositionOrientationRegistry )

    return ret
