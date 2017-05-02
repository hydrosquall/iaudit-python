# Efficient Privacy-preserving Calculation of Cloud Independence

## Cameron Yick
### Collaborators: William Dower, Ennan Zhai
### Advisor: Avi Silberschatz

## Project Proposal

Today's cloud customers intend to replicate important data and states of their applications across multiple cloud providers to ensure the availability and reliability of their applications.  These seemingly reasonable reliability enhancement efforts, however, might be undermined by correlated failures resulting from infrastructure components and software vulnerabilities shared by these redundant cloud providers.  For example, a recent investigation study reported that many cloud storage providers employ a buggy Apache Thrift library.  Suppose a cloud customer rents two individual cloud storage providers (sharing the Thrift library) for redundancy.  If an attacker compromises and triggers the vulnerability within Thrift library, the two cloud providers would become unavailability simultaneously.  Even worse, cloud providers tend to keep their internal component dependencies secret due to business concerns, thus making it hard for cloud customers to diagnose the root causes of such correlated failures.

In this project, we design and develop a novel auditing system, iAudit, that can efficiently quantify the independence of inter-cloud replications through a fine-grained scheme, while preserving the business privacy of audited cloud providers.  With the help of iAudit, a cloud customer can select the most independent replication deployment for her data or application adoption, thus preventing correlated failure risks rather than diagnosing or troubleshooting root causes after failures occur - which is too late.  The key insight of iAudit is to reduce the privacy-preserving independence auditing to a private fault graph similarity computation problem.  We address the latter by implementing two novel components: a scalable fault graph analysis engine based on Weighted MaxSAT solver and a weighted private Jaccard similarity protocol inspired by weighted sampling theory. To evaluate the prototype, we will use several zoo machines to emulate different cloud providers and measure the performance of our prototype to demonstrate the efficiency.

## Links

 - Source Code: [iAudit Python Library](https://github.com/hydrosquall/iaudit-python)
 - Final Project Report [PDF](https://github.com/hydrosquall/iaudit-python/blob/master/docs/writeup.pdf)
