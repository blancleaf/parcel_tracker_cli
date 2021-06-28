# Parcel tracker cli

This is an unofficial python tool for accessing [Parcelsapp.com](https://parcelsapp.com) API from command line.
It takes a universal parcel tracking number _(or a path to a file containing 1 such number per line)_ as an argument, makes a request and displays the results.

This script is written for python3 and depends on the _requests_ library.

###Input file format:###

trackingNumber _comment_

_trackingNumber_ has to be at the beginning of the line.
The first space after the _trackingNumber_ is treated as a delimiter.
Everything after the space is considered a _comment_ and will not be sent in the request, but will be printed out along with the tracking number in the script output.

*Example:*

```
CI0020149575KA my stuff
```

CI0020149575KA is considered a tracking number, and "my stuff" is just printed as a description of it.

**Usage:** `ptracker.py <tracking_number> or <file_path>`
