# DriveOhio

## Included files overview

### Data

Directory 'Data/': contains the data used for the analysis

- 'Data/blueroute1export.json': contains the data provided for the blue route
  - This file is currently excluded from the repo due to size/I don't know if I can share it

### helper

Library with helper functions relative to our goals

- to use the functions, add the following to your script:
```py
import helper
```
- to use the functions when helper is not in the same directory as your file, add the following to your script:
```py
import sys
sys.path.append('pathToHelperDir/..')
```

### Jupyter

Used mostly for data exploration testing and visualization

### keys

Currently empty but exists to store api keys if necessary

### Utils

Contains the main scripts for the project

- main.py
  - currently uses a possible method to better split and use the data
  - The data is split by topic, and merged on timeStamp
  - Ideally all data that comes in at timestamp x, will be present in that row
