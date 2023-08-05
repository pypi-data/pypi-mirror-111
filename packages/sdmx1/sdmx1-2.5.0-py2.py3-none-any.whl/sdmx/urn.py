import re
from typing import Dict

from sdmx.model import PACKAGE, MaintainableArtefact

# Regular expression for URNs
URN = re.compile(
    r"urn:sdmx:org\.sdmx\.infomodel"
    r"\.(?P<package>[^\.]*)"
    r"\.(?P<class>[^=]*)=((?P<agency>[^:]*):)?"
    r"(?P<id>[^\(\.]*)(\((?P<version>[\d\.]*)\))?"
    r"(\.(?P<item_id>.*))?"
)

_BASE = (
    "urn:sdmx:org.sdmx.infomodel.{package}.{obj.__class__.__name__}="
    "{ma.maintainer.id}:{ma.id}({ma.version}){extra_id}"
)


def make(obj, maintainable_parent=None):
    """Create an SDMX URN for `obj`.

    If `obj` is not :class:`.MaintainableArtefact`, then `maintainable_parent`
    must be supplied in order to construct the URN.
    """
    if maintainable_parent:
        ma = maintainable_parent
        extra_id = f".{obj.id}"
    else:
        ma = obj
        extra_id = ""

    if not isinstance(ma, MaintainableArtefact):
        raise ValueError(
            f"Neither {repr(obj)} nor {repr(maintainable_parent)} are maintainable"
        )
    elif ma.maintainer is None:
        raise ValueError(f"Cannot construct URL for {repr(ma)} without maintainer")

    return _BASE.format(
        package=PACKAGE[obj.__class__], obj=obj, ma=ma, extra_id=extra_id
    )


def match(value: str) -> Dict[str, str]:
    try:
        match = URN.match(value)
        assert match is not None
    except AssertionError:
        raise ValueError(f"not a valid SDMX URN: {value}")
    else:
        return match.groupdict()
