from __future__ import annotations

import os
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, List, Optional, Union

from commonmodel.base import Schema, SchemaLike, schema_from_yaml
from loguru import logger
from basis.core.component import (
    DEFAULT_LOCAL_NAMESPACE,
    DEFAULT_NAMESPACE,
    ComponentLibrary,
    DictView,
    global_library,
)

if TYPE_CHECKING:
    from basis.core.function import (
        DataFunctionLike,
        DataFunction,
        make_function,
    )
    from basis.core.function_package import DataFunctionPackage


class ModuleException(Exception):
    pass


class BasisModule:
    namespace: str
    py_module_path: Optional[str]
    # py_module_name: Optional[str]
    function_paths: List[str] = ["components/functions"]
    schema_paths: List[str] = ["components/schemas"]
    library: ComponentLibrary
    dependencies: List[BasisModule]

    def __init__(
        self,
        namespace: str,
        py_module_path: Optional[str] = None,
        py_module_name: Optional[str] = None,
        function_paths: List[str] = ["functions"],
        schema_paths: List[str] = ["schemas"],
        flow_paths: List[str] = ["flows"],
        dependencies: List[
            BasisModule
        ] = None,  # TODO: support str references to external deps (will need repo hooks...)
        **kwargs: Any,
    ):
        self.namespace = namespace
        if py_module_path:
            py_module_path = os.path.dirname(py_module_path)
        self.py_module_path = py_module_path
        # self.py_module_name = py_module_name
        self.library = ComponentLibrary(namespace_precedence=[self.namespace])
        self.function_paths = function_paths
        self.schema_paths = schema_paths
        self.flow_paths = flow_paths
        self.dependencies = []
        self.function_packages = {}
        if self.py_module_path:
            self.discover_schemas()
            self.discover_functions()
            # self.discover_flows() # TODO
        for d in dependencies or []:
            self.add_dependency(d)
        # for t in tests or []:
        #     self.add_test_case(t)
        global_library.add_namespace(namespace)
        global_library.add_module(self)

    def discover_functions(self):
        from basis.core.function_package import DataFunctionPackage

        if not self.py_module_path:
            return

        for functions_path in self.function_paths:
            functions_root = Path(self.py_module_path).resolve() / functions_path
            logger.debug(f"Discovering functions in {functions_path}")
            # for loader, module_name, is_pkg in pkgutil.walk_packages(functions_root):
            #     _module = loader.find_module(module_name).load_module(module_name)

            packages = DataFunctionPackage.all_from_root_path(
                str(functions_root), namespace=self.namespace
            )
            for pkg in packages:
                logger.debug(f"Found package {pkg.name}")
                self.function_packages[pkg.name] = pkg
                self.library.add_function(pkg.function)

    def discover_schemas(self):
        if not self.py_module_path:
            return
        for schemas_path in self.schema_paths:
            schemas_root = Path(self.py_module_path).resolve() / schemas_path
            for fname in os.listdir(schemas_root):
                if fname.endswith(".yml") or fname.endswith(".yaml"):
                    with open(schemas_root / fname) as f:
                        yml = f.read()
                        self.add_schema(yml)

    def add_function_package(self, pkg: DataFunctionPackage):
        self.function_packages[pkg.name] = pkg
        self.add_function(pkg.function)

    def add_function(self, function_like: Union[DataFunctionLike, str]) -> DataFunction:
        p = self.process_function(function_like)
        self.validate_key(p)
        self.library.add_function(p)
        global_library.add_function(p)
        return p

    def add_schema(self, schema_like: SchemaLike) -> Schema:
        schema = self.process_schema(schema_like)
        self.validate_key(schema)
        self.library.add_schema(schema)
        global_library.add_schema(schema)
        return schema

    def process_function(
        self, function_like: Union[DataFunctionLike, str, ModuleType]
    ) -> DataFunction:
        from basis.core.function import (
            DataFunction,
            make_function,
            PythonCodeDataFunctionWrapper,
        )
        from basis.core.sql.sql_function import sql_function
        from basis.core.function_package import DataFunctionPackage

        if isinstance(function_like, DataFunction):
            function = function_like
        else:
            if callable(function_like):
                function = make_function(function_like, namespace=self.namespace)
            # elif isinstance(function_like, str):
            #     # Just a string, not a sql file, assume it is python? TODO
            #     function = make_function(PythonCodeDataFunctionWrapper(function_like), namespaceself.name)
            elif isinstance(function_like, ModuleType):
                # Module function (the new default)
                pkg = DataFunctionPackage.from_module(function_like)
                self.add_function_package(pkg)
                return pkg.function
                # code = inspect.getsource(function_like)
                # function = make_function(PythonCodeDataFunctionWrapper(code), namespaceself.name)
            else:
                raise TypeError(function_like)
        return function

    def process_schema(self, schema_like: SchemaLike) -> Schema:
        if isinstance(schema_like, Schema):
            schema = schema_like
        elif isinstance(schema_like, str):
            schema = schema_from_yaml(schema_like, namespace=self.namespace)
        else:
            raise TypeError(schema_like)
        return schema

    def get_schema(self, schema_like: SchemaLike) -> Schema:
        if isinstance(schema_like, Schema):
            return schema_like
        return self.library.get_schema(schema_like)

    def get_function(self, function_like: Union[DataFunction, str]) -> DataFunction:
        from basis.core.function import DataFunction

        if isinstance(function_like, DataFunction):
            return function_like
        return self.library.get_function(function_like)

    def export(self):
        pass
        # if self.py_module_name is None:
        #     raise Exception("Cannot export module, no namespace set")
        # mod = sys.modules[
        #     self.py_module_name
        # ]  # = self  # type: ignore  # sys.namespace_precedence wants a modulefinder.Module type and it's not gonna get it
        # setattr(mod, "__getattr__", self.__getattribute__)

    # Add to dir:
    # setattr(mod, "functions", self.functions)
    # setattr(mod, "schemas", self.schemas)
    # setattr(mod, "run_tests", self.run_tests)
    # setattr(mod, "namespace", self.namespace)

    def __getattr__(self):
        pass

    @property
    def schemas(self) -> DictView[str, Schema]:
        return self.library.get_schemas_view()

    @property
    def functions(self) -> DictView[str, DataFunction]:
        return self.library.get_functions_view()

    def validate_key(self, obj: Any):
        if hasattr(obj, "namespace"):
            if obj.namespace != self.namespace:
                if obj.name == "Any":
                    # TODO: remove this once fixed upstream in common model
                    return
                raise ModuleException(
                    f"Component {obj} namespace `{obj.namespace}` does not match module namespace `{self.namespace}` to which it was added"
                )

    def remove_function(self, function_like: Union[DataFunctionLike, str]):
        self.library.remove_function(function_like)

    def run_tests(self):
        from basis.testing.utils import run_test_case, TestFeatureNotImplementedError

        for name, pkg in self.function_packages.items():
            print(f"Running tests for function {name}")
            for case in pkg.get_test_cases():
                print(f"======= {case.name} =======")
                try:
                    run_test_case(case, module=self)
                except TestFeatureNotImplementedError as e:
                    logger.warning(f"Test feature not implemented yet {e.args[0]}")
                except Exception as e:
                    import traceback

                    print(traceback.format_exc())
                    print(e)
                    raise e

    def add_dependency(self, m: BasisModule):
        # if isinstance(m, BasisModule):
        #     m = m.name
        self.dependencies.append(m)


DEFAULT_LOCAL_MODULE = BasisModule(DEFAULT_LOCAL_NAMESPACE)
