typenames = []

def getTypes():
    from vnf.dom import importType
    return map(importType, typenames)
