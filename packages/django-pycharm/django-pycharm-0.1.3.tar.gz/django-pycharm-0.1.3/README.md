# django-pycharm

App for Django to run any Python script within Django context


## Installation

You can install the plugin by running

```shell
pip install django-pycharm
```

In ``settings.py`` add  ``django-pycharm`` to your ``INSTALLED_APPS``
```python
INSTALLED_APPS += ['django_pycharm']
```

## Usage

```shell
python manage.py runscript <your_script.py>
```

```shell
python manage.py install_pycharm_commands
```
