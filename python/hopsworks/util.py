import json

from hopsworks import feature_group, feature
from hopsworks.core import query, join


class QueryEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, feature.Feature):
            return {"name": o._name}
        elif isinstance(o, feature_group.FeatureGroup):
            return {"id": o._id}
        elif isinstance(o, join.Join):
            return {
                "query": o._query,
                "on": o._on,
                "leftOn": o._left_on,
                "rightOn": o._right_on,
                "type": o._join_type,
            }
        elif isinstance(o, query.Query):
            return {
                "leftFeatureGroup": o._left_feature_group,
                "leftFeatures": o._left_features,
                "joins": o._joins,
            }
        else:
            return super().default(o)


def validate_feature(ft):
    if isinstance(ft, feature.Feature):
        return ft
    elif isinstance(ft, str):
        return feature.Feature(ft)


def parse_features(feature_names):
    if isinstance(feature_names, (str, feature.Feature)):
        return [validate_feature(feature_names)]
    elif isinstance(feature_names, list) and len(feature_names) > 0:
        return [validate_feature(feat) for feat in feature_names]
    else:
        return []