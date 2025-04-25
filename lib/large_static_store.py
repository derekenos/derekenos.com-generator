
import json
import os
from collections import namedtuple
from datetime import datetime
from subprocess import call
from abc import (
    ABC,
    abstractmethod,
)

import boto3

###############################################################################
# Constants
###############################################################################

MANIFEST_FILENAME = '.lss_manifest.json'

###############################################################################
# Types
###############################################################################

Metadata = namedtuple('Metadata', ('size_mb', 'last_modified'))

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

    def save_manifest(self, manifest_data=None):
        manifest = json.load(open(MANIFEST_FILENAME, 'rb')) \
            if os.path.exists(MANIFEST_FILENAME) else {}
        manifest[self.endpoint] = manifest_data or self.manifest
        with open(MANIFEST_FILENAME, 'w') as fh:
            json.dump(manifest, fh)

    @abstractmethod
    def sync(self, fs_path, dryrun=False):
        pass

    @abstractmethod
    def exists(self, path):
        pass

    @abstractmethod
    def meta(self, path):
        pass

class S3(Store):
    LAST_MODIFIED_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    def __init__(self, config):
        super().__init__(config)
        self.s3_bucket = self.s3_url[5:].rstrip("/")
        self.client = (
            boto3.session.Session(profile_name=self.aws_profile)
            .client("s3", endpoint_url=self.aws_endpoint)
        )

    def load_manifest(self):
        """Override load_manifest() to deserialize LastModified datetime."""
        super().load_manifest()
        self.manifest = {
            path: {
                k: v if k != "LastModified" else datetime.fromisoformat(v)
                for k, v in metadata.items()
            }
            for path, metadata in self.manifest.items()
        }

    def save_manifest(self):
        """Override save_manifest() to serialize LastModified datetime."""
        super().save_manifest({
            path: {
                k: v if not isinstance(v, datetime) else v.isoformat()
                for k, v in metadata.items()
            }
            for path, metadata in self.manifest.items()
        })

    def sync(self, fs_path, dryrun=False):
        """Use subprocess.call in conjunction with aws-cli to sync the
        local large objects directory to the remote.
        """
        if not os.path.isdir(fs_path):
            raise AssertionError(f'fs_path ({fs_path}) is not a directory')
        print(f'Syncing large objects from {fs_path} to: {self.s3_url}')
        call(['aws', 's3', f'--endpoint={self.aws_endpoint}',
              f'--profile={self.aws_profile}', 'sync',
              '--follow-symlinks', '--acl=public-read',
              *(['--dryrun'] if dryrun else []),
              fs_path, self.s3_url
        ])

    def regenerate_manifest(self):
        """Regenerate self.manifest by fetching all object metadata from the
        remote store.
        """
        self.manifest = {}
        continuation_token = ""
        while True:
            res = self.client.list_objects_v2(
                Bucket=self.s3_bucket,
                ContinuationToken=continuation_token
            )
            for item in res["Contents"]:
                self.manifest[item.pop("Key")] = item
            continuation_token = res.get("NextContinuationToken")
            if not continuation_token:
                break
        self.save_manifest()

    def exists(self, path):
        """Return a bool indicating whether an object with the specified path
        exists in the bucket.
        """
        if not self.manifest:
            self.regenerate_manifest()
        return path in self.manifest

    def meta(self, path):
        """Return a Metadata object for the specified path if it exists,
        otherwise return None.
        """
        if path not in self.manifest:
            return None
        item = self.manifest[path]
        return Metadata(
            size_mb=item['Size'] / 1024 / 1024,
            last_modified=item['LastModified']
        )

def get(config):
    """Instantiate and return a store based on the type specified in config.
    """
    if config['type'] != 'S3':
        raise NotImplementedError(f'type: {config["type"]}')
    return S3(config)
