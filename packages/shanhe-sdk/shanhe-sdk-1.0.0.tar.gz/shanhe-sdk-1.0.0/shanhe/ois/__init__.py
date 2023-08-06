"""
Interface to OIS (ShanHe Object Storage).
"""

from shanhe.ois.connection import QSConnection


def connect(host, access_key_id=None, secret_access_key=None):
    """ Connect to ois by access key.
    """
    return QSConnection(access_key_id, secret_access_key, host)
