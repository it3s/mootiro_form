# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
from urlparse import urlparse
import colander as c
from mootiro_web.email_validator import DomainValidator
from mootiro_form import _


domain_validator = DomainValidator()


# Validators
# ==========


def web_url(node, val):
    '''Checks whether the value is an http or https URL.'''
    pieces = urlparse(val)
    if not all([pieces.scheme, pieces.netloc]):
        raise c.Invalid(node, _('The URL must include http or https.\nFor example, http://www.example.com'))
    if pieces.scheme not in ('http', 'https'):
        raise c.Invalid(node, _('The URL must include http or https.'))
    domain, error_message = domain_validator.validate(pieces.netloc)
    if error_message:
        raise c.Invalid(node, error_message)
