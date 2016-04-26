from django import template
register = template.Library()


@register.filter
def formatted(value, plusminus=False):
    """Usage, {{ value|formatted }} or {{ value|formatted:"True" }}"""
    try:
        s = str(int(value))
        if abs(value) >= 1000:
            l = int((len(s) - 1) / 3)
            for i in range(l, 0, -1):
                s = s[:len(s) - i * 3] + ' ' + s[len(s) - i * 3:]
        if plusminus:
            if value > 0:
                return "+%s" % s
        return s
    except:
        return value


@register.filter
def toLower(text):
    """Usage, {{ text|toLower }}"""
    return text[:1].lower() + text[1:] if text else ""
