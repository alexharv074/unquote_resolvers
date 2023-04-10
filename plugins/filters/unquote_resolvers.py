from typing import Any, Dict, List, Union

import yaml
from yaml import CSafeDumper as SafeDumper
from yaml.nodes import ScalarNode


class CustomDumper(SafeDumper):
    pass


def unquoted_tag_representer(dumper: CustomDumper, data: "Tag") -> ScalarNode:
    return dumper.represent_scalar(data.tag, data.value, style="")


class Tag:
    def __init__(self, tag: str, value: str) -> None:
        self.tag = tag
        self.value = value


CustomDumper.add_representer(Tag, unquoted_tag_representer)


def unquote_resolvers(
    data: Union[Dict, List],
    indent: int = 2,
    *args: Any,
    **kw: Any
) -> str:
    """
    Remove quotes around resolver expressions and produce nice YAML.
    """

    def process_item(item: Any) -> Any:
        if isinstance(item, str) and item.startswith("!"):
            tag_name, tag_body = item.split(" ", 1)
            return Tag(tag_name, tag_body)
        elif isinstance(item, dict):
            return process_dict(item)
        elif isinstance(item, list):
            return process_list(item)
        else:
            return item

    def process_dict(dct: Dict) -> Dict:
        for key, value in dct.items():
            dct[key] = process_item(value)
        return dct

    def process_list(lst: List) -> List:
        return [process_item(value) for value in lst]

    processed_data = process_item(data)

    try:
        transformed = yaml.dump(
            processed_data,
            Dumper=CustomDumper,
            indent=indent,
            allow_unicode=True,
            default_flow_style=False,
            **kw
        )

    except Exception as e:
        raise Exception("unquote_resolvers - %s" % str(e))

    return transformed
