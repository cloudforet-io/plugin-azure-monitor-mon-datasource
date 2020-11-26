from schematics.models import Model
from schematics.types import BaseType, ListType, DictType, StringType, UnionType, IntType, FloatType
from schematics.types.compound import ModelType

__all__ = ['MetricsResponseModel', 'MetricDataResponseModel']


class ChartOptionModel(Model):
    resource = ListType(StringType, default=[])
    description = StringType(default='')
    labels = ListType(DictType(StringType), default=[])
    view = StringType(default='FULL')

class MetricModel(Model):
    key = StringType(required=True)
    name = StringType(required=True)
    unit = DictType(StringType, required=True)
    chart_type = StringType(required=True)
    chart_options = DictType(StringType, default={})


class MetricsModel(Model):
    metrics = ListType(ModelType(MetricModel), required=True)


class MetricsResponseModel(Model):
    resource_type = StringType(required=True, default='monitoring.Metric')
    actions = ListType(DictType(StringType))
    result = ModelType(MetricsModel, required=True)


class MetricDataModel(Model):
    labels = ListType(DictType(IntType), required=True)
    values = ListType(UnionType((FloatType, IntType)), required=True)


class MetricDataResponseModel(Model):
    resource_type = StringType(required=True, default='monitoring.Metric')
    actions = ListType(DictType(StringType), serialize_when_none=False)
    result = ModelType(MetricDataModel, required=True)
