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
import keygen

# encryption
from Crypto.Hash import SHA, MD5 
from Crypto.Util import number
import mmh3 as murmur  # modern murmur hash

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
    """

    def __init__(self, cutsets, isWeighted):

        def __repr__(self):
            return "CutsetList[{}] Weight:{}".format(self.length, self.weighted)

        def __str__(self):
            return "CutsetList[{}] Weight:{}".format(self.length, self.weighted)

        # self.weighted = isWeighted

        # If using the weighted protocol, need to make copies of every item
        # if isWeighted:
        #     self.cutsets = []
        #     for cutset in cutsets:
        #         self.cutsets.extend([cutset.items] * cutset.weight)
        # else:
        self._cutsets = list(cutsets)
        # self._cutsets = [cutset.items for cutset in cutsets]
        # self.length = len(self._cutsets)

    @property
    def cutsets(self):
        for cutset in self._cutsets:
            for index in xrange(cutset.weight):    # for each item
                yield "{}{}".format(cutset.items, index)


    # Form of cutsets without weighing
    @property
    def cutsetsItems(self):
        for cutset in self._cutsets:
            yield cutset.items


    @property
    def cutsetsWeights(self):
        for cutset in self._cutsets:
            yield cutset.weight

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

# Encryption


def hash_message(message, seed, hashType='MURMUR'):
    '''
        Convert string to a 128 bit signed digest.
        Hash is not cryptographic, which is OK since the encryption happens
        at a different level of abstraction.
    '''

    if hashType == 'MURMUR':
        # mmh3.hash128('foo') # 128 bit signed int
        # hashed = murmur.hash_bytes(message)
        hashed = murmur.hash128(message, seed)
    else: # throw an error
        assert(0)
    # Not implemented yet until it's decided whether it's appropriate to 
    # hash the bits.
    # the https://en.wikipedia.org/wiki/Secure_Hash_Algorithms
    # elif hashType == "SHA":   # produces 160 bit int? Considered insecure
    #     hashed = SHA.new(message)
    # elif hashType == "MD5":   # produces 128 bits marked as insecure possibly?
    #     hashed = MD5.new(message)

    return hashed


# Initial Minhash
def minhash(message, a, b, c):
    # http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/
    """
    The coefficients a and b are randomly chosen integers less than the
    maximum value of x. c is a prime number slightly bigger than the
    maximum value of x.

    minhash(x) = (ax + b) % c

    # Because we are using 128 bit murmurhash, I am going to hardcode this:
    958619577 8359471439 3831931415 1899378973 
    """

    return (a * message + b) % c
