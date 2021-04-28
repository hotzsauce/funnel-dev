# funnelmap
---

**funnelmap** is a Python package for creating, updating, and *recording* many-to-one maps from aliases to unique ids. This small project stems from a desire to use human-readable and informative names when working with APIs that store data tables with odd 'official' names. That's just one use case though, this package could be useful wherever identifiers in different contexts all need to point to the same 'proper' term, I suppose.

## Installation
---
The source code is hosted on Github: https://github.com/hotzsauce/funnel-dev.

Install via PyPI:
```console
pip install funnelmap
```

## Dependencies
---
There are no required dependencies for this package, although `pandas` is necessary to use the `to_dataframe` method of the central `FunnelMap` object.

## Documentation
---

