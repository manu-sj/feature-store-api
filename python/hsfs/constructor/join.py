#
#   Copyright 2020 Logical Clocks AB
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import humps
from hsfs import util
from hsfs.constructor import query


if os.environ.get("HOPSWORKS_RUN_WITH_TYPECHECK", False):
    from typeguard import typechecked
else:
    from typing import TypeVar

    _T = TypeVar("_T")

    def typechecked(
        target: _T,
    ) -> _T:
        return target if target else typechecked


@typechecked
class Join:
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    FULL = "FULL"
    CROSS = "CROSS"
    LEFT_SEMI_JOIN = "LEFT_SEMI_JOIN"
    COMMA = "COMMA"

    def __init__(
        self,
        query: "query.Query",
        on: Optional[List[str]],
        left_on: Optional[List[str]],
        right_on: Optional[List[str]],
        join_type: Optional[str],
        prefix: Optional[str],
        **kwargs,
    ) -> None:
        self._query = query
        self._on = util.parse_features(on)
        self._left_on = util.parse_features(left_on)
        self._right_on = util.parse_features(right_on)
        self._join_type = join_type or self.INNER
        self._prefix = prefix

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self._query,
            "on": self._on,
            "leftOn": self._left_on,
            "rightOn": self._right_on,
            "type": self._join_type,
            "prefix": self._prefix,
        }

    @classmethod
    def from_response_json(cls, json_dict: Dict[str, Any]) -> "Join":
        json_decamelized = humps.decamelize(json_dict)

        return cls(
            query=query.Query.from_response_json(json_decamelized["query"]),
            on=json_decamelized.get("on", None),
            left_on=json_decamelized.get("left_on", None),
            right_on=json_decamelized.get("right_on", None),
            join_type=json_decamelized.get("type", None),
            prefix=json_decamelized.get("prefix", None),
        )

    @property
    def query(self) -> "query.Query":
        return self._query

    @query.setter
    def query(self, query: "query.Query") -> None:
        self._query = query

    @property
    def prefix(self) -> Optional[str]:
        return self._prefix
