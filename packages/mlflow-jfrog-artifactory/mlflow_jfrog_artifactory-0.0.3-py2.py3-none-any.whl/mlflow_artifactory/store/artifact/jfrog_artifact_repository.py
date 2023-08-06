import ftplib
import logging
import os
import posixpath
from contextlib import contextmanager
from pathlib import Path

import rtpy
from mlflow.entities.file_info import FileInfo
from mlflow.exceptions import MlflowException
from mlflow.store.artifact.artifact_repo import ArtifactRepository
from mlflow.utils.file_utils import relative_path_to_artifact_path
from six.moves import urllib


class JFrogArtifactRepository(ArtifactRepository):
    """Stores artifacts as files in a JFrog Artifactory directory."""
    is_plugin = True

    def __init__(self, artifact_uri, repo_name=None, api_key=None):
        super(JFrogArtifactRepository, self).__init__(artifact_uri)
        self.artifact_uri = artifact_uri
        #TODO: API KEY from acount
        if repo_name is not None:
            self.artifactory_repo = repo_name
            return
        
        if api_key is not None:
            self.api_key = api_key
            return

        self.artifactory_endpoint =  os.environ.get("MLFLOW_ARTIFACTORY_ENDPOINT_URL")
        self.artifactory_api_key = os.environ.get("MLFLOW_ARTIFACTORY_KEY")
        self.artifactory_repo = urllib.parse.urlparse(os.environ.get("MLFLOW_ARTIFACTORY_REPO")).geturl()

        assert self.artifactory_endpoint, 'please set MLFLOW_ARTIFACTORY_ENDPOINT_URL'
        assert self.artifactory_api_key, 'please set MLFLOW_ARTIFACTORY_KEY'
        assert self.artifactory_repo, 'please set MLFLOW_ARTIFACTORY_REPO'

        parsed = urllib.parse.urlparse(artifact_uri)
        self.config = {
            "af_url": self.artifactory_endpoint, #parsed.hostname,
            "api_key": self.artifactory_api_key, #api_key,
        }

        self.af = rtpy.Rtpy(self.config)
        # use a method
        self.r = self.af.system_and_configuration.system_health_ping()
        logging.info('Artifactory is responding: %s' % self.r)

    def ping(self):
        return self.af.system_and_configuration.system_health_ping()

    @staticmethod
    def parse_artifactory_uri(uri):
        """Parse an artifactory URI, returning (path)"""
        parsed = urllib.parse.urlparse(uri)
        if parsed.scheme != "artifactory":
             raise Exception("Not an artifactory URI: %s" % uri)
        path = parsed.path
        if path.startswith('/'):
            path = path[1:]
        return parsed.netloc, path

    def log_artifact(self, local_file, artifact_path=None):
        (netloc, artifact_dir) = self.parse_artifactory_uri(self.artifact_uri + '/model')
        artifact_dir = posixpath.join(netloc, artifact_path, artifact_dir) if artifact_path else posixpath.join(netloc, artifact_dir)
    
        if local_file.is_file():
            remote_file = posixpath.join(artifact_dir, local_file.name)
            # print('local_file')
            # print(local_file)
            request = self.af.artifacts_and_storage.deploy_artifact(self.artifactory_repo, local_file, remote_file)
        # raise MlflowException("Not implemented yet log_artifact")
 
    def log_artifacts(self, local_dir, artifact_path=None):
        p = Path(local_dir).glob('**/*')
        (netloc, artifact_dir) = self.parse_artifactory_uri(self.artifact_uri +'/model')
        artifact_dir = posixpath.join(netloc, artifact_path, artifact_dir) if artifact_path else posixpath.join(netloc, artifact_dir)
        for local_file in p:
            if local_file.is_file():
                # print('local_file')
                # print(local_file)
                # with open(local_file, 'rb') as f:
                #     print(f.read())
                remote_file = posixpath.join(artifact_dir, local_file.name)
                request = self.af.artifacts_and_storage.deploy_artifact(self.artifactory_repo, local_file, remote_file)

    def _is_directory(self, artifact_path):
        if artifact_path  == "model":
            return True
        else:
            return False

        # raise MlflowException("_is_directory not implemented yet: %s" % artifact_path)

    def list_artifacts(self, path=None):
        (netloc, artifact_dir) = self.parse_artifactory_uri(self.artifact_uri)
        infos = []
        
        if path:
            full_path = "/" + netloc + '/' +artifact_dir + '/' + path
        else:
            full_path = "/" + netloc + '/' +artifact_dir
        
        for f in self._list_files(full_path, parent=path):
            infos.append(f)
        return sorted(infos, key=lambda f: f.path)
                
    def _list_files(self, directory, parent=None):
        r = self.af.artifacts_and_storage.folder_info(self.artifactory_repo, directory)
        if 'children' in r:
            listdir = r['children']
            for file in listdir:
                if file['folder']:
                    sub_directory_rel = os.path.basename(file['uri'])
                    yield FileInfo(sub_directory_rel, True, None)
                else:
                    file_name = "/" + os.path.basename(file['uri'])
                    file_rel_path = parent + file_name   
                    r_file = self.af.artifacts_and_storage.file_info(self.artifactory_repo, directory+file_name)
                    size = int(r_file['size'])
                    yield FileInfo(file_rel_path, False, size) #todo: get size

    def _download_file(self, remote_file_path, local_path):
        (netloc, artifact_dir) = self.parse_artifactory_uri(self.artifact_uri)
        artifact_path = posixpath.join(netloc, artifact_dir, remote_file_path)
        r = self.af.artifacts_and_storage.retrieve_artifact(self.artifactory_repo, artifact_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Save the file locally
        with open(local_path, "wb") as artifact:
            artifact.write(r.content)

    def delete_artifacts(self, artifact_path=None):
        raise MlflowException("delete_artifacts not implemented yet")
