import logging
import json
from six import string_types

from yang.connector import xpath_util
from cisco_gnmi import proto, Client

log = logging.getLogger(__name__)


def get_modules(cfg):
    return cfg.get('modules', {})


def get_entries(cfg):
    entries = []
    modules = get_modules(cfg)
    for mod in modules.keys():
        entries.append({
            'namespace': modules[mod]['namespace_modules'],
            'nodes': modules[mod]['entries']
        })
    return entries


def process_xpaths(xpaths):
    # Check for GET, DELETE, or SUBSCRIBE "list"
    if len(xpaths) > 1:
        # We want the longest xpath because rest are keys
        # TODO: user could have picked a bunch of random gets
        xp = max(xpaths, key=len)
    else:
        xp = xpaths[0]
    sxp = xp.split('/')
    # Pop off last segment if it is a key
    last_seg = sxp.pop()
    next_last = sxp.pop()
    if next_last.endswith(']') and last_seg in next_last:
        xp = '/'.join(sxp + [next_last])
    return xp


def get_xpath_config(xpaths, origin):
    xp = process_xpaths(xpaths)
    gnmi_xpath = Client.parse_xpath_to_gnmi_path(xp, origin)
    return [gnmi_xpath]


def get_set_payload(msgs, origin, encoding):
    gnmi_msgs = []
    if len(msgs) > 1:
        cfgs = xpath_util.get_payload(msgs)
        for cfg in cfgs:
            if isinstance(cfg, dict):
                xpath = next(iter(cfg))
                val = cfg[xpath]
                if isinstance(val, dict):
                    val = json.dumps(val).encode('utf-8')
            elif isinstance(cfg, tuple):
                xpath, val = cfg
                if isinstance(val, dict):
                    val = json.dumps(val).encode('utf-8')
            else:
                continue
            gnmi_path = Client.parse_xpath_to_gnmi_path(xpath, origin)
            update = proto.gnmi_pb2.Update()
            update.path.CopyFrom(gnmi_path)
            if encoding == 'json_ietf':
                update.val.json_ietf_val = val
            else:
                update.val.json_val = val
            gnmi_msgs.append(update)
    else:
        msg = msgs[0]
        xpath = next(iter(msg))
        val = json.dumps(msg[xpath]).encode('utf-8')
        gnmi_path = Client.parse_xpath_to_gnmi_path(xpath, origin)
        update = proto.gnmi_pb2.Update()
        update.path.CopyFrom(gnmi_path)
        if encoding == 'json_ietf':
            update.val.json_ietf_val = val
        else:
            update.val.json_val = val
            gnmi_msgs = [update]
    return gnmi_msgs


def get_messages(message_type, cfg, prefix=False):
    gnmi_paths = []
    entries = get_entries(cfg)
    for entry in entries:
        ns, msgs = entry_to_message(message_type, entry, prefix)
        gnmi_paths.append(msgs)
    return gnmi_paths


def entry_to_message(msg_type, request, prefix):
    """Convert XML Path Language 1.0 Xpath to gNMI Xpath.

    Input modeled after YANG/NETCONF Xpaths.

    References:
    * https://www.w3.org/TR/1999/REC-xpath-19991116/#location-paths
    * https://www.w3.org/TR/1999/REC-xpath-19991116/#path-abbrev
    * https://tools.ietf.org/html/rfc6020#section-6.4
    * https://tools.ietf.org/html/rfc6020#section-9.13
    * https://tools.ietf.org/html/rfc6241

    Parameters
    ---------
    request: dict containing request namespace and nodes to be worked on.
        namespace: dict of <prefix>: <namespace>
        nodes: list of dict
                <xpath>: Xpath pointing to resource
                <value>: value to set resource to
                <edit-op>: equivelant NETCONF edit-config operation

    Returns
    -------
    tuple: namespace_modules, message dict
        namespace_modules: dict of <prefix>: <module name>
            Needed for future support.
        message dict: 4 lists containing possible updates, replaces,
            deletes, or gets derived form input nodes.
    """

    paths = []
    message = {
        "update": [],
        "replace": [],
        "delete": [],
        "get": [],
        "subscribe": []
    }
    if "nodes" not in request:
        # TODO: raw rpc?
        return paths
    else:
        namespace_modules = request.get("namespace", {})
        # Default edit-op: "update"
        # But, this could be a set "delete" with keys
        last_op = 'update'
        for node in request.get("nodes", []):
            if "xpath" not in node:
                log.error("Xpath is not in message")
            else:
                xpath = node["xpath"]
                value = node.get("value", "")
                edit_op = node.get("edit-op", "")

                for pfx, mod in namespace_modules.items():
                    if not prefix:
                        mod = ""
                    else:
                        mod += ":"
                    # Adjust prefixes of xpaths
                    xpath = xpath.replace(pfx + ":", mod)
                    if isinstance(value, string_types):
                        value = value.replace(pfx + ":", mod)

                if msg_type == 'set':
                    if not edit_op:
                        edit_op = last_op
                    else:
                        last_op = edit_op

                    if edit_op in ["update", "replace"]:
                        if value:
                            xpath_lst = xpath.split("/")
                            name = xpath_lst.pop()
                            xpath = "/".join(xpath_lst)
                            cfg = {xpath: {name: value}}
                        else:
                            cfg = {xpath: {}}
                        if edit_op == "replace":
                            if not message["replace"]:
                                message["replace"] = [cfg]
                            else:
                                message["replace"].append(cfg)
                        elif edit_op == "update":
                            if not message["update"]:
                                message["update"] = [cfg]
                            else:
                                message["update"].append(cfg)
                    elif edit_op == "delete":
                        if not message["delete"]:
                            message["delete"] = [xpath]
                        else:
                            message["delete"].append(xpath)

                elif msg_type in ['get', 'subscribe']:
                    if not message[msg_type]:
                        message[msg_type] = [xpath]
                    else:
                        message[msg_type].append(xpath)
                else:
                    log.error('gNMI message type "{0}" is invalid.'.format(
                        str(msg_type)
                    ))
    return namespace_modules, message


def path_dict_to_gnmi_path(path):
    """Convert a Path dict to a gNMI Path."""
    elems = path.get('elem', [])
    origin = path.get('origin', 'openconfig')
    gnmi_path = proto.gnmi_pb2.Path()
    gnmi_path.origin = origin

    for elem in elems:
        path_elem = None
        name = elem.get('name', '')
        key = elem.get('key', '')
        if key:
            path_elem = proto.gnmi_pb2.PathElem(name=name, key=key)
        else:
            path_elem = proto.gnmi_pb2.PathElem(name=name)
        if path_elem:
            gnmi_path.elem.append(path_elem)

    return gnmi_path


def dict_to_gnmi_message(gnmi_dict, encoding):
    path = path_dict_to_gnmi_path(gnmi_dict['path'])
    update = proto.gnmi_pb2.Update()
    update.path.CopyFrom(path)
    if 'val' in gnmi_dict:
        val = gnmi_dict.get('val', {})
        value = next(iter(val.values()))
        if encoding == 'json_ietf':
            update.val.json_ietf_val = json.dumps(value).encode('utf-8')
        else:
            update.val.json_val = json.dumps(value).encode('utf-8')
    return update


def get_gnmi_request(gnmi_path, **kwargs):
    encoding = kwargs.get('encoding', 'JSON_IETF').upper()
    data_type = kwargs.get('get_type', 'ALL').upper()
    origin = kwargs.get('origin')
    prefix = kwargs.get('prefix')
    request = proto.gnmi_pb2.GetRequest()
    request.path.extend(gnmi_path)
    request.type = proto.gnmi_pb2.GetRequest.DataType.Value(data_type)
    request.encoding = proto.gnmi_pb2.Encoding.Value(encoding)
    if prefix:
        # TODO: calculate prefix paths
        prefix_path = proto.gnmi_pb2.Path()
        prefix_path.origin = origin
        request.prefix.CopyFrom(prefix_path)
    return request


def set_gnmi_request(updates, replaces, deletes, **kwargs):
    request = proto.gnmi_pb2.SetRequest()
    origin = kwargs.get('origin')
    prefix = kwargs.get('prefix')
    if updates:
        request.update.extend(updates)
    if replaces:
        request.replaces.extend(replaces)
    if deletes:
        request.delete.extend(deletes)
    if prefix:
        # TODO: calculate prefix paths
        prefix_path = proto.gnmi_pb2.Path()
        prefix_path.origin = origin
        request.prefix.CopyFrom(prefix_path)
    return request


def iter_subscribe_request(payload):
    subscribe_request = proto.gnmi_pb2.SubscribeRequest()
    subscribe_request.subscribe.CopyFrom(payload.subscribe)
    yield subscribe_request


def subscribe_gnmi_request(gnmi_path, **kwargs):
    encoding = kwargs.get('encoding', 'JSON_IETF').upper()
    mode = kwargs.get('subscribe_mode')
    origin = kwargs.get('origin')
    prefix = kwargs.get('prefix')
    sub_mode = kwargs.get('subscribe_sub_mode')
    subscribe_request = proto.gnmi_pb2.SubscribeRequest()
    subscribe_list = proto.gnmi_pb2.SubscriptionList()
    subscribe_list.mode = proto.gnmi_pb2.SubscriptionList.Mode.Value(mode)
    subscribe_list.encoding = proto.gnmi_pb2.Encoding.Value(encoding)
    subscription = proto.gnmi_pb2.Subscription()
    subscription.mode = proto.gnmi_pb2.SubscriptionMode.Value(sub_mode)
    subscription.path.CopyFrom(gnmi_path)
    subscription.sample_interval = kwargs.get('sample_interval')
    if prefix:
        # TODO: calculate prefix paths
        prefix_path = proto.gnmi_pb2.Path()
        prefix_path.origin = origin
        subscribe_list.prefix.CopyFrom(prefix_path)
    subscribe_list.subscription.extend([subscription])
    subscribe_request.subscribe.CopyFrom(subscribe_list)
    return subscribe_request
