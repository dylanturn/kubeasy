import os
from cdk8s import App, Chart

from celery import Celery

from kubeasy_sdk import EasyChart
from kubeasy_sdk.utils.collections.chart_resource_collection import ChartResourceCollection

builder_app = Celery('builder', broker=os.getenv('KUBEASY_BROKER_URI', 'pyamqp://guest@localhost//'))

@builder_app.task()
def build_chart(chart: EasyChart):
    app = App()
    combined_resource_collection = ChartResourceCollection.combine([chart.service_collection, chart.ingress_collection])
    return chart.__EasyChart(app, chart.deployment, combined_resource_collection).to_json()