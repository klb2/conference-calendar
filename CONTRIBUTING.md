# How to Contribute

Contributions are welcome and very much appreciated.

There are multiple ways in which you can contribute to the project.


## Report Bugs
Please report bugs by opening a new issue on Github.

If you are reporting a bug, please include the following information:

- Version of the package and the versions of the required packages
- Your operating system
- Detailed steps to reproduce the bug


If the bug/issue is on the website, please include the following information:

- IEEE Society/Conference name
- Link to the website with the correct information

## Fix Bugs
Any open issue that is tagged with "bug" is open to whoever wants to fix it.


## Adding More IEEE Conferences or Fixing Dates
You can always add new conferences to the website and update the dates for
existing ones.

Please make sure to follow these guidelines:

1. Create a new file for a new society in the `data` directory, e.g.,
   `comsoc.yml` for the Communications Society. If the society already exists,
   skip this step.
2. Add a new conference as a new item in the YAML file. Each conference needs
   the following keys
   - `name`: Full name of the conference
   - `abbreviation`: Abbreviation/acronym of the conference
   - `url`: URL to the conference website
   - `topic`: Topics of the conference. Currently, the keys `Communications`,
     `Signal Processing`, `Information Theory`, and `Vehicular Technology` are
     supported.
   - `type`: Type/size of the conference. Currently, the keys `flagship`,
     `conference`, and `workshop` are supported.
   - `description`: Full description of the scope of the conference.
   - `dates`: Sequence of tuples which contain the start and end dates of the
     conference.
   - `deadline`: List of deadline dates.
