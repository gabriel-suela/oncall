from _typeshed import Incomplete
from icalendar import compat as compat
from icalendar.caselessdict import CaselessDict as CaselessDict
from icalendar.parser_tools import DEFAULT_ENCODING as DEFAULT_ENCODING
from icalendar.parser_tools import SEQUENCE_TYPES as SEQUENCE_TYPES
from icalendar.parser_tools import to_unicode as to_unicode
from icalendar.prop import vText as vText

def escape_char(text): ...
def unescape_char(text): ...
def tzid_from_dt(dt): ...
def foldline(line, limit: int = ..., fold_sep: str = ...): ...
def param_value(value): ...

NAME: Incomplete
UNSAFE_CHAR: Incomplete
QUNSAFE_CHAR: Incomplete
FOLD: Incomplete
uFOLD: Incomplete
NEWLINE: Incomplete

def validate_token(name) -> None: ...
def validate_param_value(value, quoted: bool = ...) -> None: ...

QUOTABLE: Incomplete

def dquote(val): ...
def q_split(st, sep: str = ..., maxsplit: int = ...): ...
def q_join(lst, sep: str = ...): ...

class Parameters(CaselessDict):
    def params(self): ...
    def to_ical(self, sorted: bool = ...): ...
    @classmethod
    def from_ical(cls, st, strict: bool = ...): ...

def escape_string(val): ...
def unescape_string(val): ...
def unescape_list_or_string(val): ...

class Contentline(compat.unicode_type):
    strict: Incomplete
    def __new__(cls, value, strict: bool = ..., encoding=...): ...
    @classmethod
    def from_parts(cls, name, params, values, sorted: bool = ...): ...
    def parts(self): ...
    @classmethod
    def from_ical(cls, ical, strict: bool = ...): ...
    def to_ical(self): ...

class Contentlines(list):
    def to_ical(self): ...
    @classmethod
    def from_ical(cls, st): ...