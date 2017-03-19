"""
iaudit.py
Cameron Yick
March 18, 2017

iaudit is a system for independent auditing of vulnerability overlaps between
cloud providers.
"""

# import os
# import sys

# For file parsing
from lxml import objectify

# Handle multi-node deployment issues
import network

class Cutset:
    """
        # Cutset of vulernabilities that would break
        the application on a given node.
        # Each cutset has a weight, indicating its significance.
        Higher score = more significance.
        # A cutset assumes that all items have been sorted in nondescending
        # lexicographic order.
        # all weights must be integers.
    """

    # Printed and interactive console Representation
    def __repr__(self):
        return "Cutset({}, {})".format(self.items, self.weight)

    def __str__(self):
        return "Cutset: items: [{}]; weight {}".format(self.items, self.weight)

    def __init__(self, items, weight):
        self.items = items  # no need to split for now. maybe hash later
        self.weight = int(weight)


class CutsetList():
    """
        A collection of cutsets
        we will need a weighted representation of all the items inside.
        Weights are not used inside the computation
    """

    def __init__(self, cutsets, isWeighted):

        def __repr__(self):
            return "CutsetList[{}] Weight:{}".format(self.length, self.weighted)

        def __str__(self):
            return "CutsetList[{}] Weight:{}".format(self.length, self.weighted)

        self.weighted = isWeighted

        # If using the weighted protocol, need to make copies of every item
        if isWeighted:
            self.cutsets = []
            for cutset in cutsets:
                self.cutsets.extend([cutset.items] * cutset.weight)
        else:
            self.cutsets = [cutset.items for cutset in cutsets]

        self.length = len(self.cutsets)

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


def string_to_cutsets(string, isWeighted=False):
    """
        Return iterable of cutsets. Presently a list for simplicity, but
        could be replaced with a set generator.
        By default, conducts regular protocol (no weights)
    """
    return CutsetList(lxml_to_cutsets(string_to_lxml(string)), isWeighted)
    # return CutsetList(list(lxml_to_cutsets(string_to_lxml(string))))
