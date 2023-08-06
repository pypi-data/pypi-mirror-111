# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

packages = \
['lib']

package_data = \
{'': ['*']}

modules = \
['__init__']
install_requires = \
['Pillow>=8.3.0,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'robotframework>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['carrot-executor = carrot_executor:main']}

setup_kwargs = {
    'name': 'carrot-executor',
    'version': '0.6.0',
    'description': 'Camunda external task Robot Framework execution scheduler',
    'long_description': 'Camunda external task Robot Framework execution scheduler\n=========================================================\n\n**Technology preview.**\n\n`carrot-executor` is a decoupled Camunda external task executor concept for scheduling Robot Framework RPA tasks. The concept separates task locking from the execution scheduling.\n\n[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgQ2Fycm90LT4-Q2FtdW5kYTogRmV0Y2ggYW5kIGxvY2tcbiAgICBDYW11bmRhLS0-PkNhcnJvdDogVGFza1xuICAgIENhcnJvdC0-PitFeGVjdXRvcjogU2NoZWR1bGVcbiAgICBDYXJyb3QtPj5FeGVjdXRvcjogUG9sbCBzdGF0dXNcbiAgICBFeGVjdXRvci0tPj5DYXJyb3Q6IFtwZW5kaW5nXVxuICAgIENhcnJvdC0-PkNhbXVuZGE6IEV4dGVuZCBsb2NrXG4gICAgRXhlY3V0b3ItPj4rUm9ib3Q6IEV4ZWN1dGVcbiAgICBSb2JvdC0-PkNhbXVuZGE6IEdldCB0YXNrIHZhcmlhYmxlXG4gICAgQ2FtdW5kYS0tPj5Sb2JvdDogVmFyaWFibGUgdmFsdWVcbiAgICBSb2JvdC0-PkNhbXVuZGE6IFNldCB0YXNrIHZhcmlhYmxlXG4gICAgUm9ib3QtPj5DYW11bmRhOiBDb21wbGV0ZSB0YXNrXG4gICAgUm9ib3QtLT4-LUV4ZWN1dG9yOiBbZXhpdCBjb2RlXVxuICAgIENhcnJvdC0-PkV4ZWN1dG9yOiBQb2xsIHN0YXR1c1xuICAgIEV4ZWN1dG9yLS0-Pi1DYXJyb3Q6IFtjb21wbGV0ZWRdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjp0cnVlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6dHJ1ZX0)](https://mermaid-js.github.io/mermaid-live-editor/edit#)\n\nIn this concept, Carrot external task client, based on [camunda-external-task-client-js](https://github.com/camunda/camunda-external-task-client-js) fetches tasks from Camunda, schedules the execution, and keeps the task locked until the executor has completed. But the Carrot external task client only completes task when the scheduling fails for unexpected reason, by creating an incident. Any other interaction with Camunda is done by the scheduled Robot Framework bot.\n\nThis initial preview provides support for local parallel task execution, but the concept is designed to support also remote executors, like parameterized Nomad tasks, CI systems, Docker or even Robocloud API.\n\nRequirements:\n\n* Docker with Docker Compose\n\n* Python >= 3.8\n\n  ```bash\n  $ python --version\n  Python 3.8.8\n  ```\n\n* NodeJS >= 12\n\n  ```\n  $ node --version\n  v12.21.0\n  ```\n\n\nTrying it out\n=============\n\nWhile `carrot-executor` has been released at PyPI, trying out the concept requires setting up Camunda BPM Platform and Robot Framework task suites.\n\nThe easies way for that is to clone or download the project repository and starting the preconfigured Camunda with Docker Compose:\n\n```bash\n$ git clone https://github.com/datakurre/carrot-executor\n$ cd carrot-executor\n$ docker-compose up\n```\n\nAfter everything is ready, there should be Camunda running at http://localhost:8080/camunda with username `demo` and password `demo`.\n\nIn the beginning, Camunda in this demo has both theirs and ours demo processes deployed. Let\'s get rid of Camunda\'s demo process:\n\n1. Open Camunda Tasklist:http://localhost:8080/camunda/app/tasklist/default/\n2. Choose **Start process**\n3. Choose **Reset Camunda to clear state** and\n4. Press **Start**\n\nThe started process could now be completed with the help of `carrot-executor`. For that we need to create a new Python env with our package:\n\n```bash\n$ python -m venv my-carrot-executor\n$ source my-carrot-executor/bin/activate\n$ pip install carrot-executor\n```\n\nThe executor may now started with parameterizing it to complete tasks from the process we started:\n\n```bash\n$ CAMUNDA_API_PATH=http://localhost:8080/engine-rest ROBOT_SUITE=$(pwd)/robot/reset.robot CAMUNDA_TOPIC="Delete all tasklist filters,Delete all deployments" carrot-executor\npolling\n✓ subscribed to topic Delete all tasklist filters\n✓ subscribed to topic Delete all deployments\npolling\n✓ polled 2 tasks\npolling\n✓ polled 0 tasks\n```\n',
    'author': 'Asko Soukka',
    'author_email': 'asko.soukka@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
