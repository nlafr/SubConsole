from subapplication.subapplication import SubApplication
import importlib 
import pkgutil


"""
        <ScriptManager class. Imports SubApplication instances from apps module.>
        Copyright (C) <2026>  <Nathan LaFrazia>

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class ScriptManager:
    def __init__(self):
        self._apps:list[SubApplication] = []
        

    @ property
    def apps(self):
        return self._apps


    def load_apps(self):
        package_name = "scripts.apps"
        package = importlib.import_module(package_name)
        apps = []

        for module_info in pkgutil.iter_modules(package.__path__):
            module_name = f"{package_name}.{module_info.name}"
            module = importlib.import_module(module_name)
            
            if hasattr(module, "APP"):
                app: SubApplication = module.APP
                apps.append(app)
    
        self._apps = apps











