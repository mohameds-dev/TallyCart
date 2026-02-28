import json, re
def parse_json_dict_from_text(full_text: str) -> dict:
    """
    Parse the json part of the text with regex and return it as dict
    """

    json_part = re.search(r'```json\n(.*)\n```', full_text, re.DOTALL).group(1)
    return json.loads(json_part)
