# -*- coding: utf-8 -*-
import os
import time

import yaml
from prometheus_client import Gauge, Counter
from prometheus_client.core import CollectorRegistry

from core import get_logger

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
metrics_registry = CollectorRegistry(auto_describe=False)

metrics_classes = {
    "counter": Counter,
    "gauge": Gauge
}


class CommonMetrics(object):
    __slots__ = ("logger", "metrics", "instant_metrics", "continus_metrics")

    def __init__(self, config=os.getenv("CONFIG", os.path.join(root, "configs", "config.yaml"))):
        with open(config) as f:
            content = f.read().strip()
        metrics_info = yaml.safe_load(content)
        name = metrics_info.get("name", "prometheus_exporter")
        metrics_defs = metrics_info.get("metrics", [])

        self.logger = get_logger(os.path.join(root, "logs", "{}.log".format(name)), name)
        self.metrics = dict()
        self.instant_metrics = []
        self.continus_metrics = []
        for item in metrics_defs:
            metric_name = item.get("name")
            metric_desc = item.get("description")
            metric_labels = item.get("labels")
            metric_type = item.get("type", "gauge")
            metric_instant = item.get("instant", True)
            if metric_instant:
                self.instant_metrics.append(metric_name)
            else:
                self.continus_metrics.append(metric_name)
            self.metrics[metric_name] = metrics_classes[metric_type](metric_name, metric_desc, metric_labels,
                                                                   registry=metrics_registry)

    def inc(self, metric_name, labels, value):
        metric_instance = self.metrics[metric_name]
        metric_instance.labels(*labels).inc(value)
        self.logger.info("metric:{}, labels:{}, value:{}".format(metric_name, labels, value))

    def set(self, metric_name, labels, value):
        metric_instance = self.metrics[metric_name]
        metric_instance.labels(*labels).set(value)
        self.logger.info("metric:{}, labels:{}, value:{}".format(metric_name, labels, value))

    def update(self):
        for key in self.instant_metrics:
            metric_instance = self.metrics[key]
            if isinstance(metric_instance, Gauge):
                self._update_gauge_metrics(key, metric_instance)
            elif isinstance(metric_instance, Counter):
                self._update_counter_metrics(key, metric_instance)
            else:
                raise Exception("Unsupported metrics type")

    def _update_counter_metrics(self, metric_name, metric_instance):
        t0 = time.time()
        values = self.counter_metric_values(metric_name)
        for item in values:
            if not item:
                continue
            labels, value = item[0], item[1]
            metric_instance.labels(*labels).inc(value)
            self.logger.info("metric:{}, labels:{}, value:{}".format(metric_name, labels, value))
        self.logger.info("metric:{}, cost_time:{}".format(metric_name, time.time() - t0))

    def _update_gauge_metrics(self, metric_name, metric_instance):
        t0 = time.time()
        values = self.gauge_metric_values(metric_name)
        for item in values:
            if not item:
                continue
            labels, value = item[0], item[1]
            metric_instance.labels(*labels).set(value)
            self.logger.info("metric:{}, labels:{}, value:{}".format(metric_name, labels, value))
        self.logger.info("metric:{}, cost_time:{}".format(metric_name, time.time() - t0))

    @staticmethod
    def counter_metric_values(metric_name):
        labels = []
        value = 1
        return [(labels, value)]

    @staticmethod
    def gauge_metric_values(metric_name):
        labels = []
        value = 1
        return [(labels, value)]

    def __str__(self):
        _str = ""
        for key in self.__slots__:
            _str += "{}={}|".format(key, getattr(self, key))
        return _str
