from _typeshed import Incomplete
from behave.formatter import sphinx_util as sphinx_util
from behave.formatter.steps import AbstractStepsFormatter as AbstractStepsFormatter
from behave.model import Table as Table

has_docutils: bool

class StepsModule:
    module_name: Incomplete
    step_definitions: Incomplete
    def __init__(
        self, module_name, step_definitions: Incomplete | None = None
    ) -> None: ...
    @property
    def name(self): ...
    @property
    def filename(self): ...
    @property
    def module(self): ...
    @property
    def module_doc(self): ...
    def append(self, step_definition) -> None: ...

class SphinxStepsDocumentGenerator:
    default_step_definition_doc: str
    shows_step_module_info: bool
    shows_step_module_overview: bool
    make_step_index_entries: bool
    make_step_labels = has_docutils
    document_separator: Incomplete
    step_document_prefix: str
    step_heading_prefix: str
    step_definitions: Incomplete
    destdir: Incomplete
    stream: Incomplete
    document: Incomplete
    def __init__(
        self,
        step_definitions,
        destdir: Incomplete | None = None,
        stream: Incomplete | None = None,
    ) -> None: ...
    @property
    def stdout_mode(self): ...
    @staticmethod
    def describe_step_definition(
        step_definition, step_type: Incomplete | None = None
    ): ...
    def ensure_destdir_exists(self) -> None: ...
    def ensure_document_is_closed(self) -> None: ...
    def discover_step_modules(self): ...
    def create_document(self, filename): ...
    def write_docs(self): ...
    def write_step_module_index(
        self, step_modules, filename: str = "index.rst"
    ) -> None: ...
    def write_step_module(self, step_module) -> None: ...
    def write_step_module_overview(self, step_definitions) -> None: ...
    @staticmethod
    def make_step_definition_index_id(step): ...
    def make_step_definition_doc(self, step): ...
    def write_step_definition(self, step) -> None: ...

class SphinxStepsFormatter(AbstractStepsFormatter):
    name: str
    description: str
    doc_generator_class = SphinxStepsDocumentGenerator
    destdir: Incomplete
    def __init__(self, stream_opener, config) -> None: ...
    @property
    def step_definitions(self): ...
    def close(self) -> None: ...
    def create_document_generator(self): ...
    def report(self) -> None: ...
