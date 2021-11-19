<h1 align="center">
    yang-implementation-fuzzer
</h1>

<p align="center">
    <a href="/../../commits/" title="Last Commit"><img src="https://img.shields.io/github/last-commit/telekom/yang-imp-fuzzer?style=flat"></a>
    <a href="/../../issues" title="Open Issues"><img src="https://img.shields.io/github/issues/telekom/yang-imp-fuzzer?style=flat"></a>
    <a href="./COPYING" title="License"><img src="https://img.shields.io/badge/License-GPL--2.0-blue.svg?style=flat"></a>
</p>

<p align="center">
  <a href="#how-to-contribute">Contribute</a> •
  <a href="#licensing">Licensing</a>
</p>

This project contains a fuzzer that parses a YANG module, connects to a NETCONF server and then walks through the YANG model data, generating random data and sending it to the NETCONF server, to test the validity of the model implementation.

## Development

To install the project, a few dependencies are required.

* boofuzz
* ncclient
* libyang-python
* rstr
* xmltodict

The process of building the project and retrieving the required dependencies is
described below.

### Build instruction

To build the project, it's best to use a python venv inside the project.

```
git clone https://github.com/telekom/yang-imp-fuzzer.git

cd yang-imp-fuzzer

python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt

pip3 install ncclient
```

### Running the fuzzer

To run the fuzzer, run the following command

```
./fuzzer/fuzzer.py --model-name ietf-system --model-namespace "urn:ietf:params:xml:ns:yang:ietf-system" --ip 172.17.0.2 --port 8
30 --user netconf --password netconf --datastore running"
```

It might be useful to specify a single XPath to fuzz, for example:

```
./fuzzer/fuzzer.py --model-name ietf-system --model-namespace "urn:ietf:params:xml:ns:yang:ietf-system" --ip 172.17.0.2 --port 8
30 --user netconf --password netconf --datastore running --fuzz-xpath "/ietf-system:system/hostname"
```

For a list of common issues that might be encountered during fuzzer use check out [common_issues.md](docs/common_issues.md)

## How to Contribute

Contribution and feedback is encouraged and always welcome. For more information about how to contribute, the project structure, as well as additional contribution information, see our [Contribution Guidelines](./CONTRIBUTING.md). By participating in this project, you agree to abide by its [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

### Code of Conduct

This project has adopted the [Contributor Covenant](https://www.contributor-covenant.org/) in version 2.0 as our code of conduct. Please see the details in our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). All contributors must abide by the code of conduct.

### Working Language

We decided to apply _English_ as the primary project language.  

Consequently, all content will be made available primarily in English. We also ask all interested people to use English as language to create issues, in their code (comments, documentation etc.) and when you send requests to us. The application itself and all end-user facing content will be made available in other languages as needed.

## Licensing

Copyright (c) 2021 Deutsche Telekom AG.

Licensed under the **GNU General Public License Version 2.0** (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License by reviewing the file [COPYING](./COPYING) in the repository or by downloading the respective version from  
[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the [COPYING](./COPYING) for the specific language governing permissions and limitations under the License.
