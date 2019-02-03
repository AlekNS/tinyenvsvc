# -*- coding: utf-8 -*-
from ..registry import Registry as GlobalRegistry
from .services import StationTimeSeries, SummaryVariable, ThresholdOvercomeVariable


class Registry:
    @classmethod
    def summary_variable(cls) -> SummaryVariable:
        return SummaryVariable(GlobalRegistry.database())

    @classmethod
    def station_timeseries(cls) -> StationTimeSeries:
        return StationTimeSeries(GlobalRegistry.database())

    @classmethod
    def threshold_overcome_variable(cls) -> ThresholdOvercomeVariable:
        return ThresholdOvercomeVariable(GlobalRegistry.database())
