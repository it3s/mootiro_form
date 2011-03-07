function make_urls(url_data) {
    return function(handler, args) {
        url = url_data[handler];
        for (var key in args) {
            url = url.replace('{' + key + '}', args[key]);
        }
        return url;
    }
}

route_url = make_urls({"noscript": "noscript", "deform/": "deform/*subpath", "email_validator": "email_validation/{action}/{key}", "form_slug": "form/{action}/s/{slug}", "form": "form/{action}/{id}", "locale": "locale/{locale}", "reset_password": "user/{action}/{slug}", "email_validation": "email_validation/{action}", "favicon": "favicon.ico", "contact": "contact", "user": "user/{action}", "entry": "entry/{action}/{id}", "category": "category/{action}/{id}", "root": "", "static/": "static/*subpath"});
