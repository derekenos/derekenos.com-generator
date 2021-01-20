
import os
from subprocess import call
from abc import (
    ABC,
    abstractmethod,
)

class Store(ABC):
    def __init__(self, config):
        """Assign the config items as instance attributes.
        """
        for k, v in config.items():
            setattr(self, k, v)

    @abstractmethod
    def sync(self, fs_path):
        pass

class S3(Store):
    def sync(self, fs_path):
        """Use subprocess.call in conjunction with aws-cli to sync the
        local large objects directory to the remote.
        """
        print(f'Syncing large objects from {fs_path} to: {self.s3_url}')
        call(['aws', 's3', f'--endpoint={self.aws_endpoint}',
              f'--profile={self.aws_profile}', 'sync',
              '--follow-symlinks', '--acl=public-read',
              fs_path, self.s3_url
        ])

def sync(config, fs_path):
    """Helper to synchronize the local large static objects directory
    to a remote store given a store config and local filesystem path.
    """
    if not os.path.isdir(fs_path):
        raise AssertionError(f'fs_path ({fs_path}) is not a directory')
    if config['type'] == 'S3':
        return S3(config).sync(fs_path)
    raise NotImplementedError(f'type: {config["type"]}')
