#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **Python version-agnostic type hint attributes** (i.e., attributes
usable for creating PEP-compliant type hints in a safe, non-deprecated manner
regardless of the Python version targeted by the active Python interpreter).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_9
from beartype._util.utilobject import SENTINEL
from typing import Any

# ....................{ ATTRS ~ declare                   }....................
# Default *ALL* signs (particularly signs with *NO* sane fallbacks) to a
# sentinel guaranteed to *NEVER* match.

# Initialized below.
HINT_PEP_ATTR_LIST: Any = SENTINEL
'''
**List sign** (i.e., arbitrary object uniquely identifying PEP-compliant list
type hints) importable under the active Python interpreter.
'''


# Initialized below.
HINT_PEP_ATTR_TUPLE: Any = SENTINEL
'''
**Tuple sign** (i.e., arbitrary object uniquely identifying PEP-compliant tuple
type hints) importable under the active Python interpreter.
'''


# Initialized below.
HINT_PEP586_ATTR_LITERAL: Any = SENTINEL
'''
**Literal sign** (i.e., arbitrary object uniquely identifying
:pep:`586`-compliant type hints) importable under the active Python
interpreter.
'''


# Initialized below.
HINT_PEP593_ATTR_ANNOTATED: Any = SENTINEL
'''
**Annotated sign** (i.e., arbitrary object uniquely identifying
:pep:`593`-compliant type metahints) importable under the active Python
interpreter.
'''

# ....................{ ATTRS ~ define                    }....................
# Signs conditionally dependent on the major version of Python targeted by
# the active Python interpreter.

# If the active Python interpreter targets at least Python >= 3.9...
if IS_PYTHON_AT_LEAST_3_9:
    from typing import Annotated, Literal  # type: ignore[attr-defined]

    # Initialize PEP 585-compliant types.
    HINT_PEP_ATTR_LIST = list
    HINT_PEP_ATTR_TUPLE = tuple

    # Initialize PEP 586-compliant types.
    HINT_PEP586_ATTR_LITERAL = Literal

    # Initialize PEP 593-compliant types.
    HINT_PEP593_ATTR_ANNOTATED = Annotated
# Else...
else:
    from typing import List, Tuple

    # Default PEP 585-compliant types unavailable under this interpreter to
    # corresponding albeit deprecated "typing" singletons.
    HINT_PEP_ATTR_LIST = List
    HINT_PEP_ATTR_TUPLE = Tuple
