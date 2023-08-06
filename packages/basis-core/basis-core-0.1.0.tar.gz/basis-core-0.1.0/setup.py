# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basis',
 'basis.cli',
 'basis.cli.commands',
 'basis.core',
 'basis.core.declarative',
 'basis.core.execution',
 'basis.core.extraction',
 'basis.core.persistence',
 'basis.core.sql',
 'basis.core.typing',
 'basis.helpers',
 'basis.helpers.connectors',
 'basis.logging',
 'basis.migrations',
 'basis.migrations.versions',
 'basis.modules',
 'basis.modules.core',
 'basis.modules.core.functions',
 'basis.modules.core.functions.accumulate',
 'basis.modules.core.functions.accumulator',
 'basis.modules.core.functions.accumulator_sql',
 'basis.modules.core.functions.dedupe_keep_latest',
 'basis.modules.core.functions.dedupe_keep_latest.tests',
 'basis.modules.core.functions.dedupe_keep_latest_dataframe',
 'basis.modules.core.functions.dedupe_keep_latest_dataframe.tests',
 'basis.modules.core.functions.dedupe_keep_latest_sql',
 'basis.modules.core.functions.dedupe_keep_latest_sql.tests',
 'basis.modules.core.functions.import_dataframe',
 'basis.modules.core.functions.import_local_csv',
 'basis.modules.core.functions.import_records',
 'basis.modules.core.functions.import_storage_csv',
 'basis.modules.core.functions.import_table',
 'basis.templates',
 'basis.templates.templates.dataspace_template.{{ cookiecutter.name }}',
 'basis.templates.templates.dataspace_template.{{ cookiecutter.name '
 '}}.functions',
 'basis.templates.templates.function_template.{{ cookiecutter.function_name }}',
 'basis.templates.templates.function_template.{{ cookiecutter.function_name '
 '}}.tests',
 'basis.templates.templates.module_template.{{ cookiecutter.name }}',
 'basis.templates.templates.module_template.{{ cookiecutter.name }}.functions',
 'basis.templates.templates.old_module_template.{{ cookiecutter.py_module_name '
 '}}',
 'basis.templates.templates.old_module_template.{{ cookiecutter.py_module_name '
 '}}.functions',
 'basis.templates.templates.sql_function_template.{{ '
 'cookiecutter.function_name }}',
 'basis.templates.templates.sql_function_template.{{ '
 'cookiecutter.function_name }}.tests',
 'basis.templates.templates.tests_template.tests',
 'basis.testing',
 'basis.utils']

package_data = \
{'': ['*'],
 'basis.modules.core': ['schemas/*'],
 'basis.templates': ['templates/dataspace_template/*',
                     'templates/flow_template/*',
                     'templates/function_template/*',
                     'templates/module_template/*',
                     'templates/old_module_template/*',
                     'templates/schema_template/*',
                     'templates/sql_function_template/*',
                     'templates/tests_template/*'],
 'basis.templates.templates.dataspace_template.{{ cookiecutter.name }}': ['flows/*',
                                                                          'schemas/*'],
 'basis.templates.templates.module_template.{{ cookiecutter.name }}': ['flows/*',
                                                                       'schemas/*']}

install_requires = \
['alembic>=1.5.5,<2.0.0',
 'backoff>=1.10.0,<2.0.0',
 'cleo>=0.8.1,<0.9.0',
 'click>=7.1.1,<8.0.0',
 'colorful>=0.5.4,<0.6.0',
 'common-model>=0.1.4,<0.2.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'datacopy>=0.1.6,<0.2.0',
 'jinja2>=3.0.0,<4.0.0',
 'loguru>=0.5.1,<0.6.0',
 'networkx>=2.4,<3.0',
 'pandas>=1.0.1,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'pydantic-sqlalchemy>=0.0.9,<0.0.10',
 'pydantic>=1.8.1,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.4.1,<2.0.0',
 'sqlparse>=0.3.1,<0.4.0',
 'strictyaml>=1.0.6,<2.0.0']

entry_points = \
{'console_scripts': ['basis = basis.cli:app']}

setup_kwargs = {
    'name': 'basis-core',
    'version': '0.1.0',
    'description': 'Functional Data Pipelines',
    'long_description': None,
    'author': 'Ken Van Haren',
    'author_email': 'kenvanharen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
