from typing import Dict, List
import json
from lightwood.api import dtype
from lightwood.encoder import BaseEncoder
from lightwood.ensemble import BaseEnsemble
from lightwood.model import BaseModel

class Feature:
    name: str = None
    dtype: dtype = None
    dependency: List[str] = None
    encoder: BaseEncoder = None

    def __init__(self):
        self.dependency = []


class Output:
    name: str = None
    dtype: dtype = None
    encoder: BaseEncoder = None
    models: List[BaseModel] = None
    ensemble: BaseEnsemble = None

    def __init__(self):
        self.models = []

class LightwoodConfig:
    features: Dict[str, Feature] = None
    output: Output = None
    cleaner: object = None
    splitter: object = None
    analyzer: object = None

    def __init__(self, dict_obj: Dict[str,object] = None):
        if dict_obj is None:
            self.features = dict()
        else:
            # TODO impl serialization for classes that contain sub-objects that need it
            self.features = dict_obj['features']
            self.output = dict_obj['output']
            self.cleaner = dict_obj['cleaner']
            self.splitter = dict_obj['splitter']
            self.analyzer = dict_obj['analyzer']

    @staticmethod
    def loads(json_str):
        config_json = json.loads(json_str)
        return LightwoodConfig(config_json)

    def dumps(self):
        return ''

class TypeInformation:
    dtypes: Dict[str,str] = None
    additional_info: Dict[str, object] = None
    identifiers: Dict[str,object] = None

    def __init__(self):
        self.dtypes = dict()
        self.additional_info = dict()
        self.identifiers = dict()

class StatisticalAnalysis:
    # Addition of stuff here pending discussion with Jorge
    pass