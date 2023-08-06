/**
 * Module for YANG Suite gNMI / gRPC client.
 */
let gnmi = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        progressBar: "#ys-progress",

        tree: "#tree",
        serviceDialog: "#gnmi-service-dialog",
        rpcOpGroup: '#ys-rpc-group',
        editOpClass: '.ytool-edit-op',
        rpcConfigClass: '.ys-cfg-rpc',
        rpcInfoTextarea: 'textarea#ys-gnmi-content',
        deviceSelect: '#ys-devices-replay',
        getType: '[name=ys-get-type]:checked',
        originType: '[name=ys-origin-type]:checked',
        otherOrigin: '#ys-origin-other',
        prefixSupport: '#ys-prefix',
        encodingType: '[name=ys-encoding-type]:checked',
        subscribeMode: '[name=ys-subscribe-mode]:checked',
        subscribeSubMode: '[name=ys-subscribe-submode]:checked',
        sampleInterval: '#ys-sample-interval',
        rawGNMI: "textarea#ys-gnmi-content",

        buildGetURI: '/gnmi/build_get/',
        buildSetURI: '/gnmi/build_set/',
        runURI: '/gnmi/run/',
        stopSessionURI: '/gnmi/stop/session/',
        runResultURI: '/gnmi/runresult/',
        runReplayURI: '/gnmi/runreplay/',
        showReplayURI: '/gnmi/showreplay/',
    };

    let c = config;     // internal alias for brevity

    /**
     * Build a dictionary of xpaths and values from the user inputs.
     * Analogous to ysnetconf.rpcmanager.getRPCConfigs().
     *
     * {
     *   origin: 'openconfig',
     *   modules: {
     *     'moduleA': {
     *       namespace_prefixes: {...},
     *       entries: [
     *         {
     *           'xpath': ...
     *           'value': ...
     *           'nodetype': ...,
     *           'datatype': ...,
     *           'edit-op': ...,
     *         },
     *         ...
     *       ]
     *     },
     *     'moduleB': { ... },
     *     ...
     *   }
     * }
     */
    // TODO: We should use a common library from yangtree to retrieve data from
    //       tree rather than creating a new function in gnmi.
    function getRequestData() {
        if (!$(c.tree).jstree(true)) {
            return;
        }

        let request = {};
        let modules = {};
        let origin = "";

        request['get_type'] = $(c.getType).val();
        origin = $(c.originType).val();
        if (origin == 'other') {
            origin = $(c.otherOrigin).val();
        }
        request['origin'] = origin;
        request['encoding'] = $(c.encodingType).val();
        request['device'] = $(config.deviceSelect).val();
        request['prefix'] = $(c.prefixSupport).prop("checked");
        /*
         * Iterate over every user selection in the Value and Operation columns
         * We know that the Value column is first, so we will see all Value
         * elements before seeing their corresponding Operation elements.
         */
        $($(c.tree).closest('.jstree-grid-wrapper')[0])
            .find($(config.rpcConfigClass + ', ' + config.editOpClass))
            .each(function(i, element) {
                /* Get the jstree node this element associates to. */
                let nodeid = element.getAttribute('nodeid');
                let node = $(c.tree).jstree(true).get_node(nodeid);
                // TODO: keys should not have name at end of xpath
                // Wrong: /my/path[key=:value"]/key
                // if (node.data.hasOwnProperty('key')) {
                //     node = $(c.tree).jstree(true).get_node(node.parent);
                // }

                /*
                 * Find the module node that owns this node.
                 * node.parents = [parent_id, grandpt_id, ..., module_id, "#"]
                 */
                let moduleid = node.parents[node.parents.length - 2];
                let moduleNode = $(c.tree).jstree(true).get_node(moduleid);

                let moduleName = moduleNode.data.module;
                /* Initialize the config data for this module if needed. */
                if (!modules[moduleName]) {
                    modules[moduleName] = {
                        namespace_modules: moduleNode.data.namespace_modules,
                        entries: {}
                    };
                }

                /* What row number of the visible jstree-grid are we in? */
                let row = $(element)
                    .closest(".jstree-grid-column")
                    .children("div")
                    .index(element.parentElement);

                /* Update existing entry for this row, or create a new one */
                let cfg = modules[moduleName].entries[row];
                if (!cfg) {
                    cfg = {xpath: node.data.xpath_pfx};
                }
                /*
                 * config.rpcConfigClass is a string like ".some-class" --
                 * strip the leading '.' to compare against class names.
                 */
                if (element.classList.contains(config.rpcConfigClass.substr(1))) {
                    if (node.data.presence == true || node.data.datatype == "empty") {
                        cfg.value = "[null]";
                    } else if (element.type == "textarea") {
                        // anyxml or anydata
                        cfg.xml_value = element.value;
                    } else if (element.type != "checkbox" && element.type != "radio") {
                        // TODO: list should not have value assigned but we are adding
                        //       keys to the end which is wrong.
                        // if (node.data.nodetype != 'list') {
                        //     cfg.value = element.value;
                        // }
                        cfg.value = element.value;
                    }
                    cfg.nodetype = node.data.nodetype;
                    cfg.datatype = node.data.basetype || node.data.datatype;
                } else {
                    /*
                     * By elimination, this element has config.editOpClass.
                     * We will have already encountered any corresponding Value
                     * for this node previously due to iteration order.
                     * If we get here and there wasn't a user-specified Value
                     * for this node, then Operation is meaningless **unless**:
                     *
                     * 1) this is a list or container node
                     * 2) this is a leaf node of type 'empty'
                     * 3) this is a leaf and the operation is 'delete'
                     */
                    if (cfg.value != undefined ||
                        node.data.nodetype == "list" ||
                        node.data.nodetype == "container" ||
                        (node.data.nodetype == "leaf" &&
                         (node.data.datatype == "empty" ||
                          element.value == "delete")
                        )
                       ) {
                        cfg['edit-op'] = element.value;
                    } else {
                        /*
                         * Not applicable - return from this inner function
                         * so that the cfg doesn't get unnecessarily added
                         * to the module.configs.
                         */
                        return;
                    }
                }
                // if (!cfg['edit-op']) {
                //     // default is merge so assign update
                //     cfg['edit-op'] = 'update';
                // }
                let exists = false;
                for (let entry of Object.entries(modules[moduleName].entries)) {
                    if (JSON.stringify(entry[1]) == JSON.stringify(cfg)) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    modules[moduleName].entries[row] = cfg;
                }
            }); /* end inner function / .each() loop */

        /*
         * Now we must make each module.entries dict into an Array
         */
        for (let moduleName in modules) {
            if (!modules.hasOwnProperty(moduleName)) {
                continue;
            }
            let module = modules[moduleName];
            module.entries = Object.values(module.entries);
        }
        if ($.isEmptyObject(modules)) {
            alert("No data selected from model.");
            return;
        }
        request['modules'] = modules;
        return request;
    };

    function buildJSON(device) {
        let data = getRequestData();
        let action = $(config.rpcOpGroup + ' .selected').attr('data-value');
        let uri;
        if (action == 'get') {
            uri = config.buildGetURI;
        } else if (action == 'subscribe') {
            uri = config.buildGetURI;
            data['subscribe_mode'] =  $(c.subscribeMode).val();
            data['subscribe_sub_mode'] =  $(c.subscribeSubMode).val();
            data['sample_interval'] =  $(c.sampleInterval).val();
        } else if (action == 'set') {
            uri = config.buildSetURI;
        }
        data['device'] = device;
        data['encoding'] = $(c.encodingType).val();
        data['action'] = action;
        data['run'] = false;
        jsonPromise(uri, data).then(function(retObj) {
            $(config.rpcInfoTextarea).val(retObj.gnmiMsgs);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function runGNMI(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }
        data = getRequestData();
        data['run'] = true;
        data['encoding'] = $(c.encodingType).val();
        data['action'] = $(config.rpcOpGroup + ' .selected').attr('data-value');
        if (data['action'] == 'subscribe') {
            data['subscribe_mode'] =  $(c.subscribeMode).val();
            data['subscribe_sub_mode'] =  $(c.subscribeSubMode).val();
            data['sample_interval'] =  $(c.sampleInterval).val();
        }

        $.when(jsonPromise(config.runURI + device, data))
        .then(function(retObj) {
            if (!retObj) {
                popDialog("<pre>RUN " + data['action'].toUpperCase() + " failed</pre>");
                winref.close();
                return;
            }
            if (retObj.response) {
                popDialog("<pre>" + retObj.response + "</pre>");
                winref.close();
                return;
            }
        })
        .fail(function(retObj) {
            popDialog("<pre>Status: " + retObj.status + "\n" + retObj.statusText + "</pre>");
            winref.close();
        });

        let winref = window.open(
            config.runResultURI + device, device,
            "height=700 overflow=auto width=800, scrollbars=yes"
        );
    };

    function runCapabilities(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }

        let pb = startProgress($(config.progressBar)) || $(config.progressBar);

        return jsonPromise(config.runURI + device, data).then(function(retObj) {
            stopProgress(pb);
            return retObj;
        }, function(retObj) {
            stopProgress(pb);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function stopSession(device) {
        return jsonPromise(config.stopSessionURI + device);
    }

    function runReplay(device, data) {
        if (!device) {
            popDialog("Please select a device");
            return;
        }

        let pb = startProgress($(config.progressBar)) || $(config.progressBar);

        return jsonPromise(config.runReplayURI + device, data).then(function(retObj) {
            stopProgress(pb);
            return retObj;
        }, function(retObj) {
            stopProgress(pb);
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    };

    function showReplay(data) {
        data['get_type'] = $(c.getType).val();
        data['origin'] = $(c.originType).val();

        jsonPromise(config.showReplayURI, data).then(function(retObj) {
            let replay = '';
            let segments = retObj["gnmi_replay"];
            for (let segment of segments) {
                replay +=  stringify(segment) + "\n";
            }
            $(config.rpcInfoTextarea).val(replay);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    }

    /**
     * Public API.
     */
    return {
        config:config,
        buildJSON: buildJSON,
        runGNMI: runGNMI,
        stopSession: stopSession,
        runCapabilities: runCapabilities,
        runReplay: runReplay,
        showReplay: showReplay,
    };
}();
