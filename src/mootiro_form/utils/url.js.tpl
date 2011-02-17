function make_urls(url_data) {
    return function(handler, args) {
        url = url_data[handler];
        for (var key in args) {
            url = url.replace('{' + key + '}', args[key]);
        }
        return url;
    }
}

route_url = make_urls(%s);
