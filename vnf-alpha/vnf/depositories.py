

external_depositories = []


def depositories(contentroot):
    return standard_depositories(contentroot) + external_depositories



def standard_depositories(root, excludes = ['data', '.svn']):
    entries = [os.path.join(root, e) for e in os.listdir(root)]
    directories = filter(
        lambda entry: entry not in excludes and os.path.isdir(entry),
        entries)
    return directories


import os
