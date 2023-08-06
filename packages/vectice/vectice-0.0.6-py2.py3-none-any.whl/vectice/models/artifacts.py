from typing import Optional

from .code_version_artifact import CodeVersionArtifact
from .dataset_version_artifact import DatasetVersionArtifact
from .model_version_artifact import ModelVersionArtifact


class Artifacts:
    """
    factory class for Artifacts.
    """

    @classmethod
    def create_dataset_version(
        cls,
        description: Optional[str] = None,
    ) -> DatasetVersionArtifact:
        """create an artifact for a dataset"""
        return DatasetVersionArtifact.create(description)

    @classmethod
    def create_model_version(
        cls,
        description: Optional[str] = None,
    ) -> ModelVersionArtifact:
        """create an artifact for a model"""
        return ModelVersionArtifact.create(description)

    @classmethod
    def create_code_version(cls, path: str = ".") -> Optional[CodeVersionArtifact]:
        """
        create a code artifact based on the git information relative to the given local path.

        :param path: the path to look for the git repository
        :return: a CodeVersion or None if a git repository was not found locally
        """
        return CodeVersionArtifact.create(path)

    @classmethod
    def create_code_version_with_github_uri(
        cls, uri: str, script_relative_path: Optional[str] = None, login_or_token=None, password=None, jwt=None
    ) -> Optional[CodeVersionArtifact]:
        """
        create a code artifact based on the github information relative to the given URI and relative path.

        Note: The URi given can include the branch you are working on. otherwise, the default repository branch will be used.

        sample :
            https://github.com/my-organization/my-repository (no branch given so using default branch)
            https://github.com/my-organization/my-repository/tree/my-current-branch (branch given is my-current-branch)

        To access private repositories, you need to authenticate with your credentials.
        see https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/about-authentication-to-github

        :param uri: the uri of the repository with a specific branch if needed.
        :param script_relative_path:  the file that is executed
        :param login_or_token: real login or personal access token
        :param password: the password
        :param jwt: the Oauth2 access token
        :return: a CodeVersion or None if the github repository was not found or is not accessible
        """
        return CodeVersionArtifact.create_from_github_uri(uri, script_relative_path, login_or_token, password, jwt)
