<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# db_core portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_db_core/master?logo=python)](
    https://gitlab.com/ae-group/ae_db_core)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_db_core)](
    https://pypi.org/project/ae-db-core/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_db_core/coverage.svg)](
    https://ae-group.gitlab.io/ae_db_core/coverage/ae_db_core_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_db_core/mypy.svg)](
    https://ae-group.gitlab.io/ae_db_core/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_db_core/pylint.svg)](
    https://ae-group.gitlab.io/ae_db_core/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_db_core)](
    https://pypi.org/project/ae-db-core/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_db_core)](
    https://pypi.org/project/ae-db-core/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_db_core)](
    https://pypi.org/project/ae-db-core/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_db_core)](
    https://pypi.org/project/ae-db-core/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_db_core)](
    https://libraries.io/pypi/ae-db-core)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_db_core)](
    https://pypi.org/project/ae-db-core/#files)


## installation


execute the following command to use the ae.db_core module in your
application. it will install ae.db_core into your python (virtual) environment:
 
```shell script
pip install ae-db-core
```

if you instead want to contribute to this portion then first fork
[the ae_db_core repository at GitLab](https://gitlab.com/ae-group/ae_db_core "ae.db_core code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_db_core):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.db_core.html#module-ae.db_core
"ae_db_core documentation").

<!-- common files version 0.2.77 deployed version 0.2.12 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_db_core module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-db-core as namespace portion ae-db-core.
-->
