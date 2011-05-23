function dict() {
    // Makes route_url() calls possible inside jquery templates.
    // Call like this: dict('key1', 'val1', 'pi', 3.1415)
    var d = {};
    var k = null;
    for (var i = 0; i < arguments.length; i++) {
        if (k) {
            d[k] = arguments[i];
            k = null;
        } else {
            k = arguments[i];
        }
    }
    if (k && window.console) console.log('dict() got an odd number of args!');
    return d;
}

function makeUrlFuncs(url_data) {
    durl = function(handler, args) {
        var url = url_data[handler];
        for (var key in args) {
            url = url.replace('{' + key + '}', args[key]);
        }
        return url;
    }
    // jurl is easier to use than route_url because action is always present:
    // jurl(<name>, <action>, key1, val1, key2, val2...)
    jurl = function() {
        // Copy arguments to args
        var args = [];
        for (var i = 0; i < arguments.length; i++) {
            args.push(arguments[i]);
        }
        var name = args.shift();
        args.unshift('action');
        var s = url_data[name];
        while (args.length > 1) {
            var key = args.shift();
            var val = args.shift();
            s = s.replace('{' + key + '}', val);
        }
        return s;
    }
}

makeUrlFuncs(%s);
schemeDomainPort = "%s";
if (!schemeDomainPort)
    schemeDomainPort = window.location.protocol + "//" + window.location.host;
