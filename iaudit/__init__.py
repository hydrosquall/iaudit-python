
# import os
# import sys

from lxml import objectify

# Handle multi-node deployment issues
import network

class Cutset:
    """
        # A cutset is a list of vulernabilities that would break
        the application on a given node.
        # Each cutset has a weight, indicating its significance.
        Higher score = more significance.
    """

    # Printed and interactive console Representation
    def __repr__(self):
        return "Cutset({}, {})".format(self.items, self.weight)

    def __str__(self):
        return "Cutset: items: [{}]; weight {}".format(self.items, self.weight)

    def __init__(self, items, weight):
        self.items = items  # no need to split for now. maybe hash later
        self.weight = int(weight)


# Parsing
# =================
def string_to_lxml(xml):
    """
        Convert XML string to a walkable lxml object
    """
    return objectify.fromstring(xml)


def lxml_to_cutsets(obj):
    """
        Convert lxml object to cutset generator
    """
    for item in obj.cutset:
        yield Cutset(item.attrib.get('items'), item.attrib.get('weight'))


def string_to_cutsets(string):
    """
        Cutset generator
    """
    return list(lxml_to_cutsets(string_to_lxml(string)))
