# Tracking
This Folder contains everything you'll need to know about Tracking, and
analyzing the data in Python.

## Export information from RAW files

To work with the data in python, you'll need to convert it into a readable
format. If you do not have a `.txt` file to work with yet,
you'll have to use the `TextWriter` module of corryvreckan.

If you already have a `.txt` file, you can skip the next step.

Into the `run.sh` write down the following two modules

```config
[EventLoaderEUDAQ2]
file_name = "data/run@RunNumber@.raw"

[TextWriter]
file_name = "output@RunNumber@.txt"
include = "Pixel"
```

This will write all the pixel hit information neatly organized into a `.txt`
file, making it ready for manual analysis.

## Analyzing the data within Python

The basics (mostly python basics), root tutorial and the json folder are for you to get familiar with data analysis and handling scripts. If you are already have advanced programming skills and know the structure of json files and how to handle big data, you can skip those folders.

The python scripts have most of the event building, tracking and analysis tools needed for the analysis of our cosmic data.
They are all combined and explained in the jupiter notebook file `Tracking.ipynb`, so check it out!

