# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphite_exporter']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler==3.6.3',
 'PyYAML>=5.4.1,<6.0.0',
 'prometheus-client==0.7.1',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'graphite-exporter',
    'version': '1.2.1',
    'description': 'Prometheus Graphite Exporter',
    'long_description': "## graphite_exporter\nPrometheus Graphite Exporter\n## Installation\n```Bash\npip install graphite_exporter\n```\n## Usage\n### How to run\ncan use `python -m` after install graphite_exporter\n```bash\n>> python3 -m graphite_exporter -h\n\nusage: __main__.py [-h] [-i IP] [-c CONFIG] [-p PORT] [-P LISTEN_PORT]\n                   [-l LOG_LEVEL] [-L APSCHEDULER_LOG_LEVEL]\n                   [-s SYSTEM_METRIC]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -i IP, --ip IP        graphite web ip. eg: 127.0.0.1 or 127.0.0.1,127.0.0.2\n  -c CONFIG, --config CONFIG\n                        Metric config path\n  -p PORT, --port PORT  graphite web port\n  -P LISTEN_PORT, --listen_port LISTEN_PORT\n                        graphite exporter listen port\n  -l LOG_LEVEL, --log_level LOG_LEVEL\n                        log level\n  -L APSCHEDULER_LOG_LEVEL, --apscheduler_log_level APSCHEDULER_LOG_LEVEL\n                        apscheduler log level, default warning\n  -s SYSTEM_METRIC, --system_metric SYSTEM_METRIC\n                        Select the system metric to use. System Metric: carbon\n                        _update_operations,carbon_metrics_received,carbon_comm\n                        itted_points,carbon_points_per_update,carbon_cpu_usage\n                        ,carbon_creates\n```\n### Custom Metric and Config\nThe `graphite_exporter` can be configured to translate specific dot-separated graphite metrics into labeled Prometheus metrics via YAML configuration file. \n\nAn example configuration:\n```yaml\n# base param\nglobal:\n  prefix: graphite      # prometheus metric prefix\n  interval: 1m          # collection data interval\n  from: -1min           # graphite web requests param. learn more: https://graphite.readthedocs.io/en/latest/render_api.html#from-until\n  until: now            # graphite web requests param. learn more: https://graphite.readthedocs.io/en/latest/render_api.html#from-until\n  timeout: 10           # requests timeout\n\nmetrics:\n  - metric: example.*.*.user    # graphite metric\n    name: user_cnt              # prometheus metric name\n    doc: user cnt               # prometheus metric doc \n    prefix: gaphite1\n    interval: 2m\n    from: -10min\n    until: now\n    timeout: 20\n    labels:                     # prometheus metric tag info:\n      service: ${0}             #   service: ${0}  -> {service='example'}\n      app: ${1}\n      project: ${2}\n\n  - metric: example.*.app1.dau\n    name: dau\n    doc: dau\n    # No base parameters are set, \n    # this metric base param will auto set from global base param\n    labels:\n      service_project: ${0}-${2}  # service_project: ${0}-${2} -> {service_project='example-app1'}    \n      app: ${1}\n      project: ${2}\n\n  - metric: aliasByMetric(example.*.*.dau)  # graphite return metric name: dau\n    name: dau\n    doc: dau\n    labels:\n      metric: dau    # metric only be one value: dau\n\n```",
    'author': 'So1n',
    'author_email': 'so1n897046026@gamil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/so1n/graphite_exporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
