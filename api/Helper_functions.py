

# Given a list, sorts the list by a specified field in ascending or descending specified by the method
def sortList(givenList,field, method):
    return sorted(givenList, key = lambda k: k[field], reverse = method)


def listToString(s):
    str = ""
    return str.join(s)