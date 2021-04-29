# funnelmap

**funnelmap** is a Python package for creating, updating, and *recording* many-to-one maps from aliases to unique ids. This small project stems from a desire to use human-readable and informative names when working with APIs that store data tables with odd 'official' names. That's just one use case though, this package could be useful wherever identifiers in different contexts all need to point to the same 'proper' term, I suppose.

## Installation
The source code is hosted on Github: https://github.com/hotzsauce/funnel-dev.

Install via PyPI:
```console
pip install funnelmap
```

## Dependencies
There are no required dependencies for this package, although `pandas` is necessary to use the `to_dataframe` method of the central `FunnelMap` object.

## Documentation
The core of this package revolves around the `FunnelMap` class -- essentially a suped-up dictionary with a modified initialization method -- and indeed, it inherits from `MutableMapping`, so you can treat it exactly like the built-in python `dict` class. An instance can be created with a dictionary with unique ids as its keys, and collections of  associated aliases as its values:
```python
import funnelmap as fmap

things_around_me = {
    'plant': ['hoya', 'monstera', 'wandering dude', 'pothos', 'philodendron'],
    'fruit': ('orange', 'apple', 'pear'),
    'drink': {'coffee', 'tea', 'water'}
}
fm = fmap.FunnelMap(things_around_me)

# properties of the FunnelMap
fm.ids      # ['plant', 'fruit', 'drink']
fm.aliases  # ['hoya', 'monstera', 'wandering dude', ...]

# retrieving ids from both aliases & ids
fm['coffee']        # returns 'drink'
fm['philodendron']  # returns 'plant'
fm['apple']         # returns 'apple'
fm['drink']         # returns 'drink'
```

You'll notice above that indexing into a `FunnelMap` with an id (`'drink'`) simply returns that same identifier. This reflexive property is natural because we want every term referencing the 'official' identifier to map to said id. However, in all other aspects of a Python `dict`, the `FunnelMap` performs as if its keys are only the aliases:

- the `.keys()` method returns a `KeysView` whose elements are the alaises
- iterating over a  `FunnelMap` returns its aliases
- the length of a `FunnelMap` is the number of aliases it stores

### Input/Output of FunnelMaps
Ids and aliases stored in csv & JSON files can be read in as a `FunnelMap` via the `read_csv` and `read_json` package methods:
```python
def read_csv(
	path: str,
	id_index: int = 0,
	**fmtparams
):
	"""
	construct a FunnelMap from a .csv file. the location of the id is
	determined by the `id_index` parameter, and aliases for that id are the
	remaining elements in the same row.

	Parameters
	----------
	path : str | path-like
		location of the .csv file holding ids and aliases
	id_index : int ( = 0 )
		column index of the id's
	fmtparams : keyword arguments
	    formatting parameters that are passed to csv.reader
	"""
	
def read_json(path: str):
	"""
	construct a FunnelMap from a .json file. the JSON structure is assumed to
	be a list of dictionary elements structured like
		{
			'id' : id_0,
			'aliases' : [
				al_00, al_01, ..., al_0k
			]
		}

	Parameters
	----------
	path : str | path-like
		location of the .json file holding ids and aliases
	"""
```

`FunnelMap` also has a class method for constructing an instance from a `DataFrame` programatically:
```python
def from_dataframe(
	self, 
	df : DataFrame,
	ids: str = 'index',
):
	"""
	construct a FunnelMap from a pandas DataFrame.
		
	Parameters
	----------
	df : pandas DataFrame
		DataFrame that holds ids and aliases
	ids : str ( = 'index')
		location of ids in the DataFrame. if 'index' or 'column', those axis
		labels are used as the ids, and the DataFrame entries are the aliases.
	"""
```

Finally, there are `FunnelMap` methods for writing the ids and aliases to JSON strings and `DataFrame` objects:
```python
def to_json(self, path: str = '', **kwargs):
	"""
	convert FunnelMap object to a JSON string

	Parameters
	----------
	path : str | path-like
		file path. if not provided, the JSON is returned as a string
	kwargs
		optional keywords to pass to the json constructor
    	"""

def to_dataframe(self, ids: str = 'index'):
	"""
	convert FunnelMap object to a pandas DataFrame

	Parameters
	----------
	ids : str ( = 'index' )
		accepted values are 'index' and 'column'. determines the location
		of the unique ids in the dataframe. the aliases are the entries of
		the frame
	"""
```

### Recording FunnelMaps

If you find yourself working with unintuitive or non-descriptive labels over a long period of time (as I did when working on the aforementioned API), then you might consider **recording** a `FunnelMap` of those labels, and your desired aliases. Recording a `FunnelMap` creates a JSON file within the `funnelmap` package, so that your development directories won't become cluttered with files that are meant to make your coding easier.

Each saved `FunnelMap` can be assigned to a `project` directory (still stored within the `funnelmap` package), so that multiple JSON files of the same name can exist at the same time. Those `project` directories can be further organized into `subproject` directories too, as seen below.

Recording a `FunnelMap` is as easy as using its `.record()` method:
```python
fm  = FunnelMap({'meat': ['pork', 'beef'], 'potato': {'russet'}})
fm.record(name='meat_and_potatoes')
```
The `project` parameter was not defined, so it defaults to `'meat_and_potatoes'`, thereby creating within the `funnelmap` package a JSON at `meat_and_potatoes/meat_and_potatoes.json`. If we wanted to make the project name something else, just pass it to the same record:
```python
fm = FunnelMap({'meat': ['pork', 'beef'], 'potato': {'russet'}})
fm.record(name='meat_and_potatoes', project='dinner'))

# creating a subproject within dinner directory:
fm.record(name='meat_and_potatoes', project='dinner/entree')
```

To retrieve a saved `FunnelMap`, use the package method `from_record()`:
```python
import funnelmap as fmap

fm = fmap.from_record('meat_and_potatoes', project='dinner')
print(fm.to_json()) # [{"id": "meat", "aliases": ["pork", "beef"]}, {"id": "potato", "aliases": ["russet"]}]
```














