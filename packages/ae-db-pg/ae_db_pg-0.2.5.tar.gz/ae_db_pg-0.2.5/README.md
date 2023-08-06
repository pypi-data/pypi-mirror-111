<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# db_pg portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_db_pg/master?logo=python)](
    https://gitlab.com/ae-group/ae_db_pg)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_db_pg/coverage.svg)](
    https://ae-group.gitlab.io/ae_db_pg/coverage/ae_db_pg_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_db_pg/mypy.svg)](
    https://ae-group.gitlab.io/ae_db_pg/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_db_pg/pylint.svg)](
    https://ae-group.gitlab.io/ae_db_pg/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_db_pg)](
    https://libraries.io/pypi/ae-db-pg)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_db_pg)](
    https://pypi.org/project/ae-db-pg/#files)


## installation


execute the following command to use the ae.db_pg module in your
application. it will install ae.db_pg into your python (virtual) environment:
 
```shell script
pip install ae-db-pg
```

if you instead want to contribute to this portion then first fork
[the ae_db_pg repository at GitLab](https://gitlab.com/ae-group/ae_db_pg "ae.db_pg code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_db_pg):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.db_pg.html#module-ae.db_pg
"ae_db_pg documentation").

<!-- common files version 0.2.77 deployed version 0.2.4 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_db_pg module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-db-pg as namespace portion ae-db-pg.
-->
