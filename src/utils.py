import fnmatch
import logging
import os
import zlib
from os.path import exists, isfile, join

logger = logging.getLogger(__name__)


def getFilesystemPath(root, nodePath):
    """Get the on-disk path given a metric name
    :param nodePath: A metric name e.g. ``carbon.agents.graphite-a.cpuUsage``
    :returns: The path on disk"""
    return join(root, nodePath.replace('.', os.sep))


def find(pattern, path):
    """Find all files that matches the patter in a 
    given directory
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


# todo: UnicodeDecodeError while reading file
def gzip_archive(file_path):
    pass
    # if exists(file_path):
    #     try:
    #         with open(file_path) as f_in:
    #             with open(file_path+'.gz', 'wb') as f_out
    #                 compressed_data = zlib.compress(
    #                     f_in.read(), zlib.Z_BEST_COMPRESSION)
    #                 f_out.write(compressed_data)

    #         if isfile(file_path):
    #             os.remove(file_path)
    #     except Exception:
    #         raise
    # else:
    #     logger.error("File path doesn't exists")
