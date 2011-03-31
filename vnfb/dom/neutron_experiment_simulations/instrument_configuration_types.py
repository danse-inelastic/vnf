typenames = []

def getTypes():
    from vnfb.dom import importType
    return map(importType, typenames)
