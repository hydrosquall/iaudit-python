# iAudit INDaaS (Independence as a Service)
## Private, Independent Audits of Alternative Inter-Cloud Replication Deployments 

Customers of modern cloud services deploy replicas of their applications 
in order to improve reliability and performance. These replicas may be spread 
across multiple providers, such as Amazon AWS and Microsoft Azure.

Shared vulnerabilities (both hardware and software) of providers can lead to 
cascading failures, since the benefits of redundancy are lost. Despite this risk 
to consumers, cloud providers are reluctant to share vulnerability information 
with other providers. How can we let consumers achieve sufficient redundancy 
in their application deployments, while also recognizing the business concerns
of cloud providers?

Introducing  **iAudit**. 

**iAudit** is a system for computing the weighted shared dependency score
between multiple cloud providers, which does not require any of the providers
to disclose their vulnerabilities to the customer or competing providers. Lower
score indicates higher independence. Higher independence scores indicate deployment schemes with higher  application reliability.

There are two components to the system. This repository contains Python
code for the second, with influence from the [Java](https://github.com/ennanzhai/auditor) implementation.

1. Generation of provider dependency graphs
2. Compute dependency scores using a Weighted Private Set Intersection Cardinality Protocol (Vaidya and Clifton)

Part of a senior project at Yale University.

### iAudit Team
- Project Lead: [Ennan Zhai, PhD](http://www.cs.yale.edu/homes/zhai-ennan/)
- Advisor: [Profesor Avi Silberschatz](http://codex.cs.yale.edu/avi/)
- Students: William Dower, [Cameron Yick](www.cameronyick.us)

### Usage

Setup:

```
    pip install -r requirements.txt
```

Then, configure `iaudit-master.json` with your workers and desired strength of encryption.

```python
# Example configuration
{
    "masterHost": "localhost:4999",  # an unused port for master
    "keyBits": 256,                  # number of bits for encryption. minimum 256
    "modBits": 1024,                 # number of bits on p,q. minimum 512, must be even
    "workers" : [                    # unused port for workers
        "127.0.0.1:5001",
        "127.0.0.1:5002",
        "127.0.0.1:5003"
    ],
    "hashSeed": 14                  # random integer for seeding murmurhash.
    "isMinHash": 0,                 # 1 for using minHash method, 0 otherwise
    "numMinHashes": 10,             # number of minhash functions to use
    "minHashPrime": 958619577835947143938319314151899378973 # a hardcoded prime bigger than 2^128
}
```

There are 2 data directories provided here as examples.

- `master` directory simulates the log files of the master node
- `workers` directory simulates the log files of each of the `n` workers

Each worker directory, named with the worker node's ID number (from 0 to `n`),
should contain an vulnerabilities file called `vulnerabilities.txt`

To run the single-computer demo:

For each worker, spawn a worker server, using the 1st arg to specify worker id.

```
    python worker.py 0
    python worker.py 1
    python worker.py 2
```

Then, spawn the master

```
    python master.py
```

Lastly, use `trigger.py` to compute the intersection cardinalities.

```
    python trigger.py
```

You can test all this in one script with

```
    ./demo.sh
```