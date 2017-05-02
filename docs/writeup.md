# Efficient Privacy-preserving Calculation of Cloud Independence
## Cameron Yick
### Advisers: Avi Silbershatz

### Motivation

Today's cloud customers intend to replicate important data and states of their applications across multiple cloud providers to ensure the availability and reliability of their applications.  These seemingly reasonable reliability enhancement efforts, however, might be undermined by correlated failures resulting from infrastructure components and software vulnerabilities shared by these redundant cloud providers.  For example, a recent investigation study reported that many cloud storage providers employ a buggy Apache Thrift library.  Suppose a cloud customer rents two individual cloud storage providers (sharing the Thrift library) for redundancy.  If an attacker compromises and triggers the vulnerability within Thrift library, the two cloud providers would become unavailability simultaneously.  Even worse, cloud providers tend to keep their internal component dependencies secret due to business concerns, thus making it hard for cloud customers to diagnose the root causes of such correlated failures.

### System Design

In this project, we design and develop a novel auditing system, iAudit, that can efficiently quantify the independence of inter-cloud replications through a fine-grained scheme, while preserving the business privacy of audited cloud providers.  With the help of iAudit, a cloud customer can select the most independent replication deployment for her data or application adoption, thus preventing correlated failure risks rather than diagnosing or troubleshooting root causes after failures occur -- which is too late.  The key insight of iAudit is to reduce the privacy-preserving independence auditing to a private fault graph similarity computation problem.  We address the latter by implementing two novel components: a scalable fault graph analysis engine based on Weighted MaxSAT solver and a weighted private Jaccard similarity protocol inspired by weighted sampling theory. To evaluate the prototype, we will use several zoo machines to emulate different cloud providers and measure the performance of our prototype to demonstrate the efficiency.

My collaborator William Dower implemented the first component, he documents his results in a separate project. In this report, I document the design and results with implementing the second component, the weighted private Jaccard similiarity protocol. 

### Implementation Details

There are 4 primary code files involved with the protocol:
- `setup.py`

- `worker.py`
- `master.py`
- `trigger.py`

### Performance Results

The original plan of testing the scheme on the multiple machines on the Zoo cluster could not be realized due to a firewall restriction on inter-node communications. However, equivalent benchmark tests were conducted on a single zoo computer to achieve the following results.

#### Effect of Increased Input Size

![inputs_graph](graph1.png)

As anticipated, the intersection compute time scales linearly with an increase of the size of the inputs cutset on each worker node. This highlights the importance of 

We have not yet investigated the s

### Brief Discussion of Future Work
