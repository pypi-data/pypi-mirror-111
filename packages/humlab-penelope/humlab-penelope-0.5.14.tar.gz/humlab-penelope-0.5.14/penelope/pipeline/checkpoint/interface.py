import abc
import copy
import csv
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, List, Optional, Union

from penelope.corpus import DocumentIndex, Token2Id
from penelope.utility import create_instance, dictify

from ..interfaces import ContentType, DocumentPayload
from ..tagged_frame import TaggedFrame

SerializableContent = Union[str, Iterable[str], TaggedFrame]

CHECKPOINT_OPTS_FILENAME = "options.json"
DOCUMENT_INDEX_FILENAME = "document_index.csv"
DICTIONARY_FILENAME = "dictionary.csv"

# pylint: disable=too-many-instance-attributes


@dataclass
class CheckpointOpts:

    content_type_code: int = 0

    document_index_name: str = field(default=DOCUMENT_INDEX_FILENAME)
    document_index_sep: str = field(default='\t')

    sep: str = '\t'
    quoting: int = csv.QUOTE_NONE
    custom_serializer_classname: Optional[str] = None
    deserialize_in_parallel: bool = field(default=False)
    deserialize_processes: int = field(default=4)
    deserialize_chunksize: int = field(default=4)

    text_column: str = field(default="text")
    lemma_column: str = field(default="lemma")
    pos_column: str = field(default="pos")
    extra_columns: List[str] = field(default_factory=list)
    index_column: Union[int, None] = field(default=0)

    # abort_at_index: int = field(default=None)

    @property
    def props(self):
        return dictify(self)

    @property
    def content_type(self) -> ContentType:
        return ContentType(self.content_type_code)

    @content_type.setter
    def content_type(self, value: ContentType):
        self.content_type_code = int(value)

    def as_type(self, value: ContentType) -> "CheckpointOpts":
        opts = copy.copy(self)
        opts.content_type_code = int(value)
        return opts

    @staticmethod
    def load(data: dict) -> "CheckpointOpts":
        opts = CheckpointOpts()
        for key in data.keys():
            if hasattr(opts, key):
                setattr(opts, key, data[key])
        return opts

    @property
    def custom_serializer(self) -> type:
        if not self.custom_serializer_classname:
            return None
        return create_instance(self.custom_serializer_classname)

    @property
    def columns(self) -> List[str]:
        return [self.text_column, self.lemma_column, self.pos_column] + (self.extra_columns or [])

    def text_column_name(self, lemmatized: bool = False):
        return self.lemma_column if lemmatized else self.text_column


@dataclass
class CheckpointData:
    source_name: Any = None
    content_type: ContentType = ContentType.NONE
    document_index: DocumentIndex = None
    token2id: Token2Id = None
    create_stream: Callable[[], Iterable[DocumentPayload]] = None
    checkpoint_opts: CheckpointOpts = None
    filenames: List[str] = None


class IContentSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, content: SerializableContent, options: CheckpointOpts) -> str:
        ...

    @abc.abstractmethod
    def deserialize(self, content: str, options: CheckpointOpts) -> SerializableContent:
        ...
