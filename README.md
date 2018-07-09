# Archive metric data from carbon

Archiving metric data of a given metric group from start timestamp to end timestamp using the render url API.

### Running the application

To use the application, run:
```bash
cd src/
python3 archive_metric.py <cmd-line args>
```
##### Available command line arguments
```
usage: archive_metric.py [-h] [-mg METRIC_GROUP] [-st FROMT] [-et UNTILT]
                         archive-path

archive metric group

positional arguments:
  archive-path          specify the archive directory

optional arguments:
  -h, --help            show this help message and exit
  -mg METRIC_GROUP, --metric-group METRIC_GROUP
                        metric group to archive
  -st FROMT, --fromt FROMT
                        start timestamp in unix time
  -et UNTILT, --untilt UNTILT
                        end timestamp in unix time
```