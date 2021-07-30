# Track Analysis and Visualization in Python # 

## trackAnalysisLib.py: ##
Python function library for reading/analyzing/plotting JSON Files written by corryvreckan. A functional description is given below.

## Examples: ## 
Usage examples with data from DESY (run000683).
- example1.py: Imports 10 pixels from the file and plots the data without using the library.
- example2.py: Plots a Straight Line Track and GBL Track with the same clusters

##  Corryvreckan JSON Data: ##
Data is imported to python using `json.load(file)`. The loaded JSON Array then contains all exported clipboard objects from the whole run set into subarrays for each event. To set only specific objects for export, use `include`:
```toml
[JSONWriter]
file_name = "exampleFileName"
include = "Cluster","Track"
```
## Dealing with the JSON Data in Python: ##
- Objects from the imported array can be sorted using the `'_typename'` key (e.g. `'corryvreckan::GblTrack'`)`.
- Objects which implement structure relations such as e.g. Tracks <-- Cluster will still contain a list of clusters. However, those Clusters are just placeholders containing the correct `'fUniqueID'`. This means, if one wants to access Cluster data (e.g. x, y coordinates), one must also export Clusters from Corryvreckan.
- Beware that Corryvreckan changes e.g. Cluster UIDs with every run. This means, generally, data from two different runs (with different settings) can not be compared - use e.g. the `findEquivalentTrackByClusters(...)` function to get another track fitted to the same clusters.

## Python Module: trackAnalysisLib ##
### Structure ###
The library is structured into three types of functionality:
1) Python class `datamanager` to deal with the JSON Data.
2) *print-* functions, to print information about clusters, tracks, ...
3) *plot-* functions to produce specific plots.
### class `datamanager` ###
JSON data can imported using `json.load(file.json)`, however, the resulting data structure is inconvenient to deal with.
The `datamanager` class can be used to obtain three flat lists `pixels`, `clusters` and `tracks` from the data, as well as list `eventMap` with an entry for each event. This map allows to reassociate the elements of the three lists to an event. Each entry contains a tuple of tuples:
`((<first pixel index>,<last pixel index>),(<first cluster index>,<last cluster index>),(<first track index>,<last track index>))`

To create an instance of `datamanager` provide the constructor a path to a datafile:
`dm=datamanager('output/data.json')`
This will read the file `output/data.json` and create the above given datastructure. The datastructure can then be saved to a file using
`dm.save('file')`.
If no file path is provided, the file will be saved under the same name with the extension `.npy`. A saved file can be loaded with 
`dm=datamanager('output/data.npy')`.
Note that giving a file extension will always result in loading this specific file. When no extension is given, e.g.:
`datamanager('output/data')`
`datamanager` will load whichever file is newer.

Additional Options:
- `update`: When no file extension is given, the data will always be read from the `.npy` file if it is avaialiable.
    default `update=False`
- `verbose`: Prints additional output when a file is read.
    default `verbose=False`
- `tempDataPath`: Sets the path where the `.npy` file will be created. `tempDataPath=''` will create the file in the same directory as the inital json file, when `dm.save()` is called.
    default `tempDataPath=''`
- `removeJSONFile`: Removes the given JSON file and automatically saves as `.npy`.
    default `removeJSONFile=False`
- `mapping`: Creates cluster to pixel and track to cluster maps. Creating the maps is slow and therefore disabled by default, but will speed up e.g. `dm.getClustersForTracks(track)`.
    default `mapping=False`

