# findts2
Copyright2019\
Script to find ts-files (transcoding-stream) on enigma2 settopboxes

## Installation:
* Copy the **_findts_** directory to **_/usr/local/_**
* Copy the **_findts2_** file to **_/usr/bin/_**
* adapt Line 74 in **_findts.py_** to your movie directory: `bashstr = "find /media/hdd/dlna/Video -iname *" + findarg + "*.ts"`

## Use:
in console:

`findts2 movie*title -parameter(s)`

_Note: use `*` instead of `space`_

### Parameters
```
Searches for the movie title in the file name

No arguments given: findts2 PartOfTheMovieFileName [-d]
 -e -E EPG data/extended data Display
 -d -D Display duration/display duration in minutes
 -n Display names
 -N Hide file name (Shows the name instead)
 -m Show metadata
 -M Hide file names, show metadata
 -a show extended meta data
 -t Show tags
 -c Show progress
 -C Cuts Displays
 -S Display total
 -h Help dialog
```