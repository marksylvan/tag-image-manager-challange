from typing import Any, Dict, List, Union

import simplejson as json
from pytest_snapshot.plugin import Snapshot


def pdump(v: Any) -> str:
    """ Pretty JSON dump helper """
    return json.dumps(v, indent=2, sort_keys=True)


def json_assert(
    collection: Union[List[str], str],
    snapshot: Snapshot,
    dir_name: Union[None, str] = None,
):
    """
    Loads each JSON from str collection into a dictionary.
    Then compares a snaphsot of the pretty-dumped json using pytest-snapshot.
    """
    if isinstance(collection, str):
        collection = [collection]

    data = [json.loads(item) for item in collection]
    return dict_assert(data, snapshot, dir_name)


def dict_assert(
    collection: Union[List[Dict[str, Any]], Dict[str, Any]],
    snapshot: Snapshot,
    dir_name: Union[None, str] = None,
):
    """
    Then compares a snaphsot of the pretty-dumped dictionary
    using pytest-snapshot.
    """
    if dir_name is None:
        dir_name = "expected"

    if isinstance(collection, dict):
        collection = [collection]

    compare_object = {
        f"{i}.json": pdump(entry) for i, entry in enumerate(collection)
    }

    snapshot.assert_match_dir(compare_object, dir_name)
