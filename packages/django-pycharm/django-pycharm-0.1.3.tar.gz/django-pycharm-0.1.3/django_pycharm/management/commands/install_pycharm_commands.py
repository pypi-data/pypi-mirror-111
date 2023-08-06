import shutil
from pathlib import Path

import xmltodict
from django.core.management.base import BaseCommand, CommandError


commands = {
    "runcommand": {
        "@name": "runcommand",
        "@type": "PythonConfigurationType",
        "@factoryName": "Python",
        "option": [
            {
                "@name": "INTERPRETER_OPTIONS",
                "@value": ""
            },
            {
                "@name": "PARENT_ENVS",
                "@value": "true"
            },
            {
                "@name": "SDK_HOME",
                "@value": ""
            },
            {
                "@name": "WORKING_DIRECTORY",
                "@value": "$PROJECT_DIR$"
            },
            {
                "@name": "IS_MODULE_SDK",
                "@value": "true"
            },
            {
                "@name": "ADD_CONTENT_ROOTS",
                "@value": "true"
            },
            {
                "@name": "ADD_SOURCE_ROOTS",
                "@value": "true"
            },
            {
                "@name": "SCRIPT_NAME",
                "@value": "$PROJECT_DIR$/manage.py"
            },
            {
                "@name": "PARAMETERS",
                "@value": "$FileNameWithoutExtension$"
            },
            {
                "@name": "SHOW_COMMAND_LINE",
                "@value": "false"
            },
            {
                "@name": "EMULATE_TERMINAL",
                "@value": "false"
            },
            {
                "@name": "MODULE_MODE",
                "@value": "false"
            },
            {
                "@name": "REDIRECT_INPUT",
                "@value": "false"
            },
            {
                "@name": "INPUT_FILE",
                "@value": ""
            }
        ],
        "envs": {
            "env": {
                "@name": "PYTHONUNBUFFERED",
                "@value": "1"
            }
        },
        "EXTENSION": {
            "@ID": "PythonCoverageRunConfigurationExtension",
            "@runner": "coverage.py"
        },
        "method": {
            "@v": "2"
        }
    },

    "runscript": {
        "@name": "runscript",
        "@type": "PythonConfigurationType",
        "@factoryName": "Python",
        "option": [
            {
                "@name": "INTERPRETER_OPTIONS",
                "@value": ""
            },
            {
                "@name": "PARENT_ENVS",
                "@value": "true"
            },
            {
                "@name": "SDK_HOME",
                "@value": ""
            },
            {
                "@name": "WORKING_DIRECTORY",
                "@value": "$PROJECT_DIR$"
            },
            {
                "@name": "IS_MODULE_SDK",
                "@value": "true"
            },
            {
                "@name": "ADD_CONTENT_ROOTS",
                "@value": "true"
            },
            {
                "@name": "ADD_SOURCE_ROOTS",
                "@value": "true"
            },
            {
                "@name": "SCRIPT_NAME",
                "@value": "$PROJECT_DIR$/manage.py"
            },
            {
                "@name": "PARAMETERS",
                "@value": "runscript $FilePath$"
            },
            {
                "@name": "SHOW_COMMAND_LINE",
                "@value": "false"
            },
            {
                "@name": "EMULATE_TERMINAL",
                "@value": "false"
            },
            {
                "@name": "MODULE_MODE",
                "@value": "false"
            },
            {
                "@name": "REDIRECT_INPUT",
                "@value": "false"
            },
            {
                "@name": "INPUT_FILE",
                "@value": ""
            }
        ],
        "envs": {
            "env": {
                "@name": "PYTHONUNBUFFERED",
                "@value": "1"
            }
        },
        "EXTENSION": [
            {
                "@ID": "PythonCoverageRunConfigurationExtension",
                "@runner": "coverage.py"
            }
        ],
        "method": {
            "@v": "2"
        }
    }
}




class Command(BaseCommand):
    help = 'Install Pycharm run configurations for debugging Django'

    def find_command(self, runmanager, command_name):
        if not isinstance(runmanager["configuration"], list):
            runmanager["configuration"] = [runmanager["configuration"]]

        for command in runmanager["configuration"]:
            if command["@name"] == command_name:
                return command

    def add_commands(self, runmanager):
        for command_name, snippet in commands.items():
            if self.find_command(runmanager, command_name):
                self.stdout.write(self.style.NOTICE(f"Command '{command_name}' already exists"))
            else:
                runmanager["configuration"] = list(runmanager["configuration"]) + [snippet]
                self.stdout.write(self.style.SUCCESS(f"Command '{command_name}' added"))
        return runmanager


    def handle(self, *args, **options):
        idea_config = Path(".").resolve() / ".idea" / "workspace.xml"
        if not idea_config.is_file():
            raise CommandError("PyCharm configuration not found. Please setup project first")

        config = xmltodict.parse(idea_config.read_text('utf-8'))
        if config["project"]["@version"] != "4":
            raise CommandError("Incompatible PyCharm version")

        config["project"]["component"] = [
            self.add_commands(component) if component["@name"] == "RunManager" else component
            for component in config["project"]["component"]
        ]

        shutil.copy(str(idea_config), str(idea_config) + ".bak")
        xmltodict.unparse(
            config,
            output=idea_config.open("w"),
            pretty=True
        )
