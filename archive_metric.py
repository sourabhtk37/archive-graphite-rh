import argparse
import logging.config
import os
import struct
import sys
from os.path import isdir, join

import requests

from utils import getFilesystemPath, gzip_archive

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="archive metric group")

request_url = "http://localhost/render?target={mg}&format=json&from={st}&until={et}"

DIR_PERMS = 0o755
if not isdir(sys.argv[1]):
    os.mkdir(sys.argv[1], DIR_PERMS)
ARCHIVE_PATH = sys.argv[1]
DATAPOINT_SIZE = struct.calcsize('!d')


# todo: implement file seek to resuse the file and gap management
def write_data(datapoints, args):
    """Write to archive file

    Creates a nested directory from metric group name. Name of file is 
    created from beginning timestamp and resolution(seconds per points) which is 
    of format `timestamp@resolution`. The data is stored as list of big-endian 
    double precision floats. The timestamps for each datapoints are calculated as 
    `beginning timestamp + datapoint offset * resolution`.

    :params datapoints: list of datapoints with timestamps
    :params args: cmd-line argument parameters
    :returns :str: archive file path
    """

    fsPath = getFilesystemPath(ARCHIVE_PATH, args.metric_group)

    if not isdir(fsPath):
        os.makedirs(fsPath, mode=DIR_PERMS)

    resolution = datapoints[1][1] - \
        datapoints[0][1]
    beg_timestamp = datapoints[0][1]

    values = [v for v, t in datapoints]
    format = '!' + ('d' * len(values))
    packedValues = struct.pack(format, *values)

    file_path = join(fsPath, "{ts}@{rsol}".format(
        ts=beg_timestamp, rsol=resolution))
    logging.debug("Writing to file: {0}".format(file_path))
    with open(file_path, 'w+b') as fileHandle:
        try:
            fileHandle.write(packedValues)
        except Exception:
            raise

    return file_path


# todo: read implementation
def read_data(file_path):
    """Read archive
    :params file_path: archive file to be read
    """
    pass


def request_metric_data(args):
    """Retrieve data from graphite

    :params args: cmd-line argument parameters
    :returns :list: metric datapoints
    """
    metric_data = requests.get(request_url.format(
        mg=args.metric_group, st=args.fromt, et=args.untilt))

    return metric_data.json()


def main():
    """Driver function
    """
    args = parser.parse_args()
    metric_data = request_metric_data(args)

    try:
        file_path = write_data(metric_data[0]['datapoints'], args)
    except IOError:
        logging.error("Unable to write to archive")
        exit(1)

    # gzip_archive(file_path)


if __name__ == '__main__':
    parser.add_argument("archive-path",
                        help="specify the archive directory")
    parser.add_argument("-mg", "--metric-group",
                        help="metric group to archive")
    parser.add_argument("-st", "--fromt", type=int,
                        help="start timestamp in unix time")
    parser.add_argument("-et", "--untilt", type=int,
                        help="end timestamp in unix time")
    main()
