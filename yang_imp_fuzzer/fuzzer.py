#!/usr/bin/env python3
#
# telekom / yang-imp-fuzzer
#
# Copyright (c) 2021 Deutsche Telekom AG
#
# Deutsche Telekom AG and all other contributors / copyright 
# owners license this file to you under the terms of the GPL-2.0:
#
# yang-imp-fuzzer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as published by
# the Free Software Foundation.
#
# yang-imp-fuzzer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yang-imp-fuzzer. If not, see <https://www.gnu.org/licenses/
#

import argparse
import boofuzz
import libyang
import xmltodict
import sys
import yang_imp_fuzzer.yangprimitives

class ModuleParser:
    def __init__(self, modules_dir, module_path, namespace, capabilities, conn, fuzz_xpath):
        self.module_path = module_path
        self.namespace = namespace
        self.conn = conn
        self.fuzz_xpath = fuzz_xpath

        self.ctx = libyang.Context(modules_dir)
        self.module = self.ctx.load_module(module_path)
        self.version = self.parse_yang_version(self.module.filepath())

        self.enabled_features = self.get_enabled_features(capabilities, self.version)

        self.enable_local_features()

    def enable_local_features(self):
        module_features = list(self.module.features())
        module_features = [f.name() for f in module_features]

        for f in self.enabled_features:
            if f in module_features:
                self.module.feature_enable(f)

    def parse_yang_version(self, filepath):
        with open(filepath)as f:
            for line in f:
                statement = line.strip()
                elements = statement.split()
                if len(elements) == 2 and elements[0] == "yang-version":
                    if elements[1] == "1.1;":
                        return "1.1"
        return "1.0"

    def get_enabled_features(self, capabilities, version):
        if version == "1.0":
            for c in capabilities:
                if "?module=" + self.module.name() + "&" in c:
                    return self.parse_features(c)
        elif version == "1.1":
            namespace = {"ly": "urn:ietf:params:xml:ns:yang:ietf-yang-library"}
            select = "/ly:yang-library"
            xml = self.conn.get(filter=("xpath", (namespace, select))).data_xml
            modules = xmltodict.parse(xml)['data']['yang-library']['module-set']['module']
            if self.module.name() not in [m['name'] for m in modules]:
                sys.exit("module not found on remote server")
            for m in modules:
                if m['name'] == self.module.name():
                    if isinstance(m['feature'], str):
                        return [m['feature']]
                    else:
                        return m['feature']

        return []

    def parse_features(self, capability):
        features = capability.split("&features=")

        if len(features) < 2:
            return []

        features = features[1]

        return features.split(",")

    def parse_module(self):
        nodes = []
        for c in self.module.children():
            if not c.config_false():
                node = self.parse_top_level_node(c)
                if node is not None:
                    nodes.append(node)

        return nodes

    def parse_top_level_node(self, node):
        config_start = boofuzz.Static(default_value="""<nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">""")
        config_end = boofuzz.Static(default_value="</nc:config>")
        res = [] 

        if self.fuzz_xpath is not None and node.data_path() not in self.fuzz_xpath:
            return None

        if node.keyword() in ['container', 'list', 'rpc']:
            res.append(config_start)
            res.extend(self.parse_container_node(node, True))
        else:
            res.extend(self.parse_data_node(node))

        res.append(config_end)
        node = boofuzz.Request(node.name(), children=res)
        return node

    def parse_nested_node(self, node):
        config_start = boofuzz.Static(default_value="""<nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">""")
        config_end = boofuzz.Static(default_value="</nc:config>")
        res = [] 

        if self.fuzz_xpath is not None and node.data_path() not in self.fuzz_xpath:
            return res

        if node.keyword() in ['container', 'list', 'rpc']:
            res.extend(self.parse_container_node(node, False))
        else:
            res.extend(self.parse_data_node(node))

        return res

    def parse_container_node(self, node, namespace):
        res = []

        if self.fuzz_xpath is not None and node.data_path() not in self.fuzz_xpath:
            return res

        if namespace:
            res.append(boofuzz.Static(default_value="<" + node.name() + " xmlns=\"" + self.namespace + "\">"))
        else:
            res.append(boofuzz.Static(default_value="<" + node.name() + ">"))

        for c in node.children():
            if c.config_false():
                continue
            res.extend(self.parse_nested_node(c))

        res.append(boofuzz.Static(default_value="</" + node.name() + ">"))

        return res

    def parse_data_node(self, node):
        res = []

        if self.fuzz_xpath is not None and node.data_path() not in self.fuzz_xpath:
            return res

        res.append(boofuzz.Static(name=node.name() + "start", default_value="<" + node.name() + ">"))
        res.append(self.handle_data_node_type(node))

        res.append(boofuzz.Static(name=node.name() + "end", default_value="</" + node.name() + ">"))

        return res

    def handle_data_node_type(self, node):
        node_type = node.type()

        if node_type.base() == libyang.Type.UNION:
            return self.handle_union_node(node_type, node.name())
        elif node_type.base() == libyang.Type.ENUM:
            return self.handle_enum_node(node_type, node.name())
        else:
            return self.handle_primitive_node(node_type, node.name())

    def handle_primitive_node(self, node, name):
        max_val, min_val, patterns = self.handle_data_restriction_stmts(node)

        if min_val and max_val:
            if patterns:
                return yangprimitives.yang_boofuzz_map[node.base()](name=name + "data", min_val=min_val, max_val=max_val, patterns=patterns)
            else:
                return yangprimitives.yang_boofuzz_map[node.base()](name=name+ "data", min_val=min_val, max_val=max_val)
        else:
            if patterns:
                return yangprimitives.yang_boofuzz_map[node.base()](name=name + "data", patterns=patterns)
            else:
                return yangprimitives.yang_boofuzz_map[node.base()](name=name + "data")

    def handle_enum_node(self, node, name):
        enum_vals = [e[0] for e in node.all_enums()]
        return yangprimitives.yang_boofuzz_map[libyang.Type.ENUM](name=name + "data", enum_vals=enum_vals)

    def handle_union_node(self, node, name):
        children = [self.handle_primitive_node(n, name + "child" + str(i)) for i, n in enumerate(node.union_types())]
        return yangprimitives.yang_boofuzz_map[libyang.Type.UNION](name=name + "data", children=children)

    def handle_data_restriction_stmts(self, node_type):
        max_val = None
        min_val = None
        patterns = None

        if node_type.length() is not None:
            length = node_type.length().split("..")
            min_val = length[0]
            max_val = length[1]
        elif node_type.range() is not None:
            length = node_type.range().split("..")
            min_val = length[0]
            max_val = length[1]

        if any(node_type.patterns()):
            patterns = list(node_type.patterns())[0]

        return max_val, min_val, patterns

def parse_args():
    parser = argparse.ArgumentParser(description="Fuzz YANG model implementation validity on a remote NETCONF server")
    parser.add_argument('--model-name', dest='model_path', type=str, required=True, help='Path to the model to use for data generation')
    parser.add_argument('--model-namespace', dest='model_namespace', type=str, required=True, help='Namespace of model to use for data generation')
    parser.add_argument('--modules-directory', dest='modules_dir', type=str, default='/usr/share/yang/modules', help='Path to the directory with YANG modules')
    parser.add_argument('--ip', dest='ip', type=str, default='172.17.0.2', help='NETCONF target server IP address')
    parser.add_argument('--port', dest='port', type=int, default=830, help='NETCONF target server TCP port')
    parser.add_argument('--user', dest='user', type=str, default='netconf', help='NETCONF target username')
    parser.add_argument('--password', dest='password', type=str, default='netconf', help='NETCONF target password')
    parser.add_argument('--datastore', dest='datastore', type=str, default='running', help='NETCONF target datastore to fuzz')
    parser.add_argument('--fuzz-xpath', dest='fuzz_xpath', type=str, help='XPath selecting node to be fuzzed. If not specified, the whole model is fuzzed')
    return parser.parse_args()

def main():
    args = parse_args()

    conn = boofuzz.NETCONFConnection(args.ip, args.port, args.user, args.password, args.datastore, False)
    session = boofuzz.Session(target=boofuzz.Target(connection = conn))

    conn.open()
    raw_conn = conn.get_raw_conn()
    capabilities = raw_conn.server_capabilities
    parser = ModuleParser(args.modules_dir, args.model_path, args.model_namespace, capabilities, raw_conn, args.fuzz_xpath)
    nodes = parser.parse_module()
    conn.close()

    for node in nodes:
        session.connect(node)

    session.fuzz()
