import json
from typing import Any, Dict

from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.request import Formats
from google_play_scraper.utils.request import get
from google_play_scraper.exceptions import NotFoundError


def developer(developer_token: str, lang: str = "en", country: str = "us") -> Dict[str, Any]:
    url = Formats.Developer.build(developer_token, lang=lang, country=country)

    try:
        dom = get(url)
    except NotFoundError:
        url = Formats.Developer.fallback_build(developer_token, lang=lang)
        dom = get(url)

    matches = Regex.SCRIPT.findall(dom)

    dataset = {}

    for match in matches:
        key_match = Regex.KEY.findall(match)
        value_match = Regex.VALUE.findall(match)

        if key_match and value_match:
            key = key_match[0]
            value = json.loads(value_match[0])

            dataset[key] = value

    result = {}

    for k, spec in ElementSpecs.Developer.items():
        # print("SPCES", k, spec)
        if isinstance(spec, list):
            for sub_spec in spec:
                content = sub_spec.extract_content(dataset)

                if content is not None:
                    result[k] = content
                    break
        else:
            content = spec.extract_content(dataset)

            result[k] = content
    
    _d = []
    if result["apps"]:
        for x in result["apps"]:
            _d.append(x)
    if result["apps2"]:
        for y in result["apps2"]:
            _d.append(y)
    result.pop("apps2")
    
    result["apps"] =  _d
    result["url"] = url

    return result