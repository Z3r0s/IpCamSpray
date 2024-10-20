import json
from jsonpath_ng import parse as jsonpath_parse
from lxml import etree

def extract_with_xpath(xml_response, xpath_expression):
    try:
        tree = etree.fromstring(xml_response.encode())
        return tree.xpath(xpath_expression)
    except Exception as e:
        print(f"[ERROR] XPath extraction failed: {e}")
        return []

def extract_with_jsonpath(json_response, jsonpath_expression):
    try:
        json_data = json.loads(json_response)
        jsonpath_expr = jsonpath_parse(jsonpath_expression)
        return [match.value for match in jsonpath_expr.find(json_data)]
    except Exception as e:
        print(f"[ERROR] JSONPath extraction failed: {e}")
        return []