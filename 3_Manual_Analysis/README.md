# Manual Analysis
So your data is shitty eh? Well no problem at all, since there is a line of
[legends](../Media/legends.jpg)
that have come before you and did all the dirty work in advance.

## Export information from RAW files

To work with the data in python, you'll need to convert it into a readable
format. If you do not have a `.json` file to work with yet,
you'll have to use the `JSONWriter` module of corryvreckan.

If you already have a `.json` file, you can skip the next step.

Into the `run.sh` write down the following two modules

```config
[EventLoaderEUDAQ2]
file_name = "data/run@RunNumber@.raw"

[JSONWriter]
file_name = "output@RunNumber@.txt"
include = "Pixel"
```

This will write all the pixel hit information neatly organized into a `.json`
file, making it ready for manual analysis.

## Analyzing the data within Python

The basics (mostly python basics), root tutorial and the json folder are
for you to get familiar with data analysis and handling scripts. If you
are already have advanced programming skills and know the structure of
json files and how to handle big data, you can skip those folders.

The `scripts` folder contains all of the event building, tracking and analysis
tools needed for the analysis of our cosmic data.
They are all combined and explained in the `Tutorial.ipynb`
[jupiter notebook file](Tutorial.ipynb), so check it out!

