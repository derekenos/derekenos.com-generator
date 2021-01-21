
import json
import os
from http import client
from subprocess import call
from abc import (
    ABC,
    abstractmethod,
)

###############################################################################
# Constants
###############################################################################

MANIFEST_FILENAME = '.lss_manifest.json'

###############################################################################
# Classes
###############################################################################

class Store(ABC):
    def __init__(self, config):
        """Assign the config items as instance attributes.
        """
        for k, v in config.items():
            setattr(self, k, v)
        # manifest is a path -> response.headers map that keeps track of
        # which objects exist in the remote store.
        self.manifest = {}
        self.load_manifest()

    def load_manifest(self):
        if os.path.exists(MANIFEST_FILENAME):
            manifest = json.load(open(MANIFEST_FILENAME, 'rb'))
            if self.endpoint in manifest:
                self.manifest.update(manifest[self.endpoint])

    def save_manifest(self):
        manifest = json.load(open(MANIFEST_FILENAME, 'rb')) \
            if os.path.exists(MANIFEST_FILENAME) else {}
        manifest[self.endpoint] = self.manifest
        with open(MANIFEST_FILENAME, 'w') as fh:
            json.dump(manifest, fh)

    @abstractmethod
    def sync(self, fs_path):
        pass

    @abstractmethod
    def exists(self, path):
        pass

class S3(Store):
    def sync(self, fs_path):
        """Use subprocess.call in conjunction with aws-cli to sync the
        local large objects directory to the remote.
        """
        if not os.path.isdir(fs_path):
            raise AssertionError(f'fs_path ({fs_path}) is not a directory')
        print(f'Syncing large objects from {fs_path} to: {self.s3_url}')
        call(['aws', 's3', f'--endpoint={self.aws_endpoint}',
              f'--profile={self.aws_profile}', 'sync',
              '--follow-symlinks', '--acl=public-read',
              fs_path, self.s3_url
        ])

    def exists(self, path):
        """Return a bool indicating whether an object with the specified path
        exists in the bucket.
        """
        if path in self.manifest:
            return True
        conn = client.HTTPSConnection(self.endpoint.split('/', 2)[2])
        conn.request('HEAD', path)
        res = conn.getresponse()
        self.manifest[path] = dict(res.headers)
        return res.status == 200

def get(config):
    """Instantiate and return a store based on the type specified in config.
    """
    if config['type'] != 'S3':
        raise NotImplementedError(f'type: {config["type"]}')
    return S3(config)
