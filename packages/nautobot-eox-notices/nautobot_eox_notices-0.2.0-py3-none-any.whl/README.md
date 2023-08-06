# nautobot-eox-notices

A plugin for [Nautobot](https://github.com/nautobot/nautobot).

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```shell
pip install nautobot-eox-notices
```

> The plugin is compatible with Nautobot 1.0.0b1 and higher

To ensure Nautobot EoX Tracker is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-eox-notices` package:

```no-highlight
# echo nautobot-eox-notices >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your `configuration.py`

```python
# In your configuration.py
PLUGINS = ["eox_notices"]

# PLUGINS_CONFIG = {
#   "eox_notices": {
#     "expired_field": "end_of_support",
#   }
# }
```

The plugin behavior can be controlled with the following list of settings.

| Setting       | Default        | Description                                                                                                                                                                                                                           |
| ------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| expired_field | end_of_support | The field that will be used to determine if an EoxNotice object is expired. If the field does not exist on the object, it will determine which of the required fields is set and use that. (Either `end_of_support` or `end_of_sale`) |

## Usage

### API

![](docs/images/eox_notice_api_view.png)

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. 

Each command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`

#### Local dev environment

```no-highlight
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart Nautobot and its dependencies.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

#### Utility

```no-highlight
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
```

#### Testing

```no-highlight
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           This will run flake8 for the specified name and Python version.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

## Screenshots

### EoX List View

You can view the list of EoX notices as well as filter the table.

![](docs/images/eox_notice_list_view.png)

> The device count is provided in the list view.

### EoX Detail View

You can also click an EoX Notice and see the detail view. This view provides links to the devices that are part affected by this EoX notice due to their device type.

![](docs/images/eox_notice_detail_view.png)

### Device View

You can also view the associated EoX notice from the device. If the device is end of life or end of supoort the notice will be red.

![](docs/images/eox_notice_device_view.png)

### Device Type View

This provides the same UI element as the device view, but within the specific device type's view.

![](docs/images/eox_notice_device_type_view.png)