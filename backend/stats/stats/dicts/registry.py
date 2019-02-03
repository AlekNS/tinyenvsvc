# -*- coding: utf-8 -*-
from ..registry import Registry as GlobalRegistry
from .services import VariablesDict, StationsDict


class Registry:
    @classmethod
    def variables_dict(cls) -> VariablesDict:
        return VariablesDict(GlobalRegistry.database())

    @classmethod
    def stations_dict(cls) -> StationsDict:
        return StationsDict(GlobalRegistry.database())
