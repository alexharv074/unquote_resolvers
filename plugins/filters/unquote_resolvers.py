import yaml
from yaml import CSafeDumper as SafeDumper

class CustomDumper(SafeDumper):
    pass

def unquoted_tag_representer(dumper, data):
    return dumper.represent_scalar(data.tag, data.value, style='')

class UnquotedTag:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

CustomDumper.add_representer(UnquotedTag, unquoted_tag_representer)

def unquote_resolvers(a, indent=4, *args, **kw):
    '''Remove quotes around resolver expressions and produce nice YAML'''

    def process_dict(d):
        for key, value in d.items():
            if isinstance(value, str) and value.startswith('!'):
                tag_name, tag_body = value.split(' ', 1)
                d[key] = UnquotedTag(tag_name, tag_body)
            elif isinstance(value, dict):
                process_dict(value)

    process_dict(a)

    try:
        transformed = yaml.dump(a, Dumper=CustomDumper, indent=indent, allow_unicode=True, default_flow_style=False, **kw)
    except Exception as e:
        raise Exception("unquote_resolvers - %s" % str(e))
    return transformed
