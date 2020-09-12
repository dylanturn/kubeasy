import os

from celery import Celery

from kubeasy_sdk import EasyChart

app = Celery('builder', broker=os.getenv('KUBEASY_BROKER_URI', 'pyamqp://guest@localhost//'))


@app.task
def build(chart: EasyChart):
    return chart.render()