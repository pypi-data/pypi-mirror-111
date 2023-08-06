from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mlflow-jfrog-artifactory",
    version="0.0.3",
    description="Artifactory plugin for MLflow for Artifact storage",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Require MLflow as a dependency of the plugin, so that plugin users can simply install
    # the plugin & then immediately use it with MLflow
    install_requires=["mlflow>=1.11", "rtpy==1.4.9"],
    python_requires='!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,<4.0,>=2.7',
    platforms='any',
    entry_points={
        "mlflow.artifact_repository": "artifactory=mlflow_artifactory.store.artifact.jfrog_artifact_repository:JFrogArtifactRepository",  # noqa
    },
    options={'bdist_wheel':{'universal':'1'}},
)
