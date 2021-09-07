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

Build instructions
=================

To build the project, it's best to use a python venv inside the project.

```
git clone git@lab.sartura.hr:sysrepo/yang-validation-fuzzer.git --recurse-submodules

cd yang-validation-fuzzer

python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt
```

Running the fuzzer
=================

To run the fuzzer, run the following command

```
python3 fuzzer/fuzzer.py --model-name ietf-system --model-namespace "urn:test"
```

Common errors
=================
If the target NETCONF server has NACM enabled the following error might appear:
```
[2021-09-07 17:25:10,692]   Test Step: Fuzzing Node 'system'
[2021-09-07 17:25:10,692]     Info: Sending 324 bytes...
[2021-09-07 17:25:10,892]     Error!!!! Unexpected exception! Traceback (most recent call last):
                                File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1388, in _main_fuzz_loop
                                  self._fuzz_current_case(mutation_context)
                                File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1754, in _fuzz_current_case
                                  self.transmit_fuzz(
                                File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1169, in transmit_fuzz
                                  self.targets[0].send(data)
                                File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 221, in send
                                  num_sent = self._target_connection.send(data=data)
                                File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/connections/netconf_connection.py", line 28, in send
                                  self.conn.edit_config(target=self.datastore, config=data)
                                File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/manager.py", line 226, in execute
                                  return cls(self._session,
                                File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/operations/edit.py", line 69, in request
                                  return self._request(node)
                                File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/operations/rpc.py", line 360, in _request
                                  raise self._reply.error
                              ncclient.operations.rpc.RPCError: Access to the data model "ietf-system" is denied because "netconf" NACM authorization failed.

Traceback (most recent call last):
  File "/home/user/yang-validation-fuzzer/./fuzzer/fuzzer.py", line 227, in <module>
    main()
  File "/home/user/yang-validation-fuzzer/./fuzzer/fuzzer.py", line 224, in main
    session.fuzz()
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1264, in fuzz
    self._main_fuzz_loop(self._generate_mutations_indefinitely(max_depth=max_depth))
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1388, in _main_fuzz_loop
    self._fuzz_current_case(mutation_context)
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1754, in _fuzz_current_case
    self.transmit_fuzz(
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 1169, in transmit_fuzz
    self.targets[0].send(data)
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/sessions.py", line 221, in send
    num_sent = self._target_connection.send(data=data)
  File "/home/user/yang-validation-fuzzer/boofuzz-fork/boofuzz/connections/netconf_connection.py", line 28, in send
    self.conn.edit_config(target=self.datastore, config=data)
  File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/manager.py", line 226, in execute
    return cls(self._session,
  File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/operations/edit.py", line 69, in request
    return self._request(node)
  File "/home/user/yang-validation-fuzzer/env/lib/python3.9/site-packages/ncclient/operations/rpc.py", line 360, in _request
    raise self._reply.error
ncclient.operations.rpc.RPCError: Access to the data model "ietf-system" is denied because "netconf" NACM authorization failed.
```

In that case either enable the appropriate NACM operations on the server for the user that is used to fuzz, or disable NACM completely.
In the case of sysrepo and Netopeer2, use the following command will disable NACM:

```
sysrepocfg -Evim -f json -m ietf-netconf-acm -d running
```

Then enter the following data into the datastore:
```
{
    "ietf-netconf-acm:nacm": {
                "enable-nacm": false
        }
}
```
