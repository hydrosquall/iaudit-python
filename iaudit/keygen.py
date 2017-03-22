# Key generation and configuration

import Crypto
from Crypto.PublicKey import RSA
from Crypto.PublicKey import pubkey
from Crypto.Util import number
import random
import json

def getConfig(filepath):
    '''
        Load configuration file
    '''
    with open(filepath, 'r') as f:
        config = json.load(f)

    return config

def setConfig(obj, filepath):
    '''
        Save object to file
    '''
    with open(filepath, 'w') as f:
        config = json.dump(obj, f)


# use p, q generation script
def generate_pq(modBits):
    '''
        Generate p, q (public key) with modBits bits for SRA encryption
        generate primes p and q, from Sefasi and pycrypt
    '''
    assert(modBits % 2 == 0) # must provide even number of bits
    p = q = 1L
    while number.size(p*q) < modBits:
            if modBits > 512 :
                    p = pubkey.getStrongPrime(modBits>>1, 0, 1e-12, None)
                    q = pubkey.getStrongPrime(modBits - (modBits>>1), 0, 1e-12, None)
            else :
                    p = pubkey.getPrime(modBits>>1, None)
                    q = pubkey.getPrime(modBits - (modBits>>1), None)

    return (p, q)

def generate_e(p, q, keyBits, seed):
    '''
        Generate e (private key) with (keyBits) bits for SRA encryption
    '''
    if p > q:
        (p, q)=(q, p)

    n = p * q
    phi = (p - 1)*(q - 1)

    # generate private key key
    e = phi
    
    # seed random generator to avoid collision
    random.seed(seed)
    while (number.GCD(e, phi) != 1) or (e >= n) :
        e = random.getrandbits(keyBits)# possibly replace with https://docs.python.org/2/library/random.html#random.SystemRandom
    return e


def generate_public_config(modBits, keyBits):
    p, q = generate_pq(modBits)

    config = {}
    config['type'] = 'public'
    config['modBits'] = modBits
    config['keyBits'] = keyBits
    config['encryption'] = {
        'p': p,
        'q': q
    } 
    return config
    
def generate_private_config(public_config, keyBits, seed):
    
    p = public_config['encryption']['p']
    q = public_config['encryption']['q']
    
    e = generate_e(p, q, keyBits, seed)
    
    config = {}
    config['type'] = 'private'
    config['keyBits'] = keyBits
    config['encryption'] = {
        'e': e
    }
    
    return config

def make_private_key(public_config, private_config):
    '''
    Args:
        public_config (dict): Contains public modulus p, q
        private_config (dict): Contains private exponent e
    Returns:
        An RSA key object (`_RSAobj`).
    
    '''
    # public key contains public modulus
    # in production, use a local public key file
    p = long(public_config['encryption']['p'])
    q = long(public_config['encryption']['q'])
    # private key contains private exponent
    e = long(private_config['encryption']['e'])

    # Enforce constraint that p must be bigger.
    # http://crypto.stackexchange.com/questions/18084/in-rsa-why-does-p-have-to-be-bigger-than-q-where-n-p-times-q
    if p < q:
        p, q = q, p
        
    # in practice, not needed 
    n = p*q
    phi = (p - 1)*(q - 1)
    d = pubkey.inverse(e, phi)
    rsaInit = (n, e, d, p, q)
    #     rsaInit = (n, e, d)
    #     print "n {}, e {}, d {}, p {}, q {}".format(n, e, d, p, q)
    return RSA.construct(rsaInit)