#!/usr/bin/env python3

import argparse
import boofuzz
import libyang
import xmltodict
import sys

class ModuleParser:
    def __init__(self, modules_dir, module_path, namespace, capabilities, conn):
        self.module_path = module_path
        self.namespace = namespace
        self.conn = conn
        self.xml_template_start="""<?xml version="1.0" encoding="UTF-8"?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0 xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">"""
        self.xml_template_end="</data>\n"

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
        for c in self.module.children():
            self.handle_child(c, 1, False)
        xml = self.xml_template_start + self.xml_template_end
        return xml.splitlines()

    def handle_child(self, child, level, indent):
        if indent:
            indentation = level * '\t'
        else:
            indentation = ""

        if child.keyword() in ['container', 'list', 'rpc']:
            if level == 1:
                self.xml_template_start += indentation + "<" + child.name() + " xmlns=\"" + self.namespace + "\">\n"
            else:
                self.xml_template_start += indentation + "<" + child.name() + ">\n"
            for c in child.children():
                self.handle_child(c, level + 1, indent)
            self.xml_template_start += indentation + "</" + child.name() + ">\n"
        else:
            self.xml_template_start += indentation + "<" + child.name() + ">\n"
            if indent:
                self.xml_template_start += indentation + "\tFUZZ\n"
            else:
                self.xml_template_start += indentation + "FUZZ\n"

            self.xml_template_start += indentation + "</" + child.name() + ">\n"

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
    return parser.parse_args()

def main():
    args = parse_args()

    conn = boofuzz.NETCONFConnection(args.ip, args.port, args.user, args.password, args.datastore)
    session = boofuzz.Session(target=boofuzz.Target(connection = conn))

    conn.open()
    raw_conn = conn.get_raw_conn()
    capabilities = raw_conn.server_capabilities
    parser = ModuleParser(args.modules_dir, args.model_path, args.model_namespace, capabilities, raw_conn)
    xml = parser.parse_module()
    conn.close()

    request_children = []

    for line in xml:
        if line == "FUZZ":
            request_children.append(boofuzz.String(default_value=line))
        else:
            request_children.append(boofuzz.Static(default_value=line))

    xml_request = boofuzz.Request("get-config", children=request_children)

    session.connect(xml_request)

    session.fuzz()

if __name__ == "__main__":
    main()


