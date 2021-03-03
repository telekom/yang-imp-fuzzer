YANG Validation Fuzzer
======================

This project contains a fuzzer that parses a YANG module,
connects to a NETCONF server and then walks through the YANG model data,
generating random data and sending it to the NETCONF server,
to test the validity of it's implementation.

Dependenices
===========

To install the projects, a few libraries are required.

* boofuzz
* ncclient
* libyang-python
