from coffin import template
register = template.Library()

import json
from jinja2 import Markup


@register.filter
def jsonify(value):
    return Markup(json.dumps(value))
