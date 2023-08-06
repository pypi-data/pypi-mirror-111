import logging
from typing import Optional, Any, List, Sequence

from vectice.adapter import Adapter
from vectice.api import Page
from vectice.api.output import JobOutput, JobRunOutput, PagedResponse
from vectice.models import (
    Artifact,
    RunnableJob,
    Job,
    JobRun,
    DatasetVersionArtifact,
    Artifacts,
    ModelVersionArtifact,
    CodeVersionArtifact,
)

logger = logging.getLogger(__name__)


# Import experiment into Vectice with all associated run (could be long !)
def save_job(project_token: str, experiment_name: str, lib: str):
    try:
        vectice = Vectice(project_token=project_token, lib=lib)
        vectice.save_job_and_associated_runs(experiment_name)
    except Exception:
        logger.exception(f"saving job {experiment_name} failed")


# Import run of experiment into Vectice
def save_after_run(
    project_token: str,
    run: Any,
    lib: Optional[str],
    inputs: Optional[List[Artifact]] = None,
    outputs: Optional[List[Artifact]] = None,
) -> Optional[int]:
    """
        save in Vectice platform information relative to this run.
        The run object can be of several type depending on which
        lib you are using.

    :param project_token: the token of the project the job is belong to
    :param run: the run we want to save
    :param lib: Name of the lib you are using (for now, None or MLFlow)
    :param inputs: list of inputs (artifact) you are using in this run
    :param outputs: list of outputs (artifact) you are using in this run
    :return: id of the saved run or None if the run can not be saved
    """
    try:
        vectice = Vectice(project_token, lib)
        return vectice.save_run(run, inputs, outputs)
    except Exception:
        logger.exception("saving run failed")
        return None


def create_run(job_name: str, job_type: Optional[str] = None) -> RunnableJob:
    """
    create a local object of a run. Note that the run is not created in
    vectice server (and as a consequence is NOT visible until saved after the run).

    This object will save any information relative to a run and its associated job.

    The returned instance need to be used with associated :func:`save_after_run`

    For job types, take a look at the list in :class:`~vectice.models.JobType`

    :param job_name: the name of the job involve in the run
    :param job_type: the type of the job involve in the run
    :return: a runnable job
    """
    if job_name is None:
        raise RuntimeError("Name of job must be provided.")
    job = Job(job_name)
    if job_type is not None:
        job.with_type(job_type)
    return RunnableJob(job, JobRun())


class Vectice(Adapter):
    """
    High level class to list jobs and runs but also save runs
    """

    def __new__(cls, project_token: str, lib: str = None, *args, **kwargs):
        if lib is not None:
            if str(lib).lower() == "mlflow":
                from vectice.adapter.mlflow import MlflowAdapter

                return MlflowAdapter(project_token=project_token, *args, **kwargs)  # type: ignore
            else:
                raise ValueError(f"Unsupported lib: {lib}")
        else:
            return super().__new__(cls)

    def __init__(self, project_token: str, lib: Optional[str] = None):
        super().__init__(project_token=project_token)

    def list_jobs(
        self, search: Optional[str] = None, page_index=Page.index, page_size=Page.size
    ) -> PagedResponse[JobOutput]:
        """
        list all jobs

        :param search: text to filter jobs base on their name
        :param page_index: index of the page we want
        :param page_size: size of the page we want
        :return: a list of filtered jobs
        """
        return self._client.list_jobs(search, page_index, page_size)

    def list_runs(self, job_id: int, page_index=Page.index, page_size=Page.size) -> Sequence[JobRunOutput]:
        """
        list all run of a specific job

        :param job_id: the Vectice job identifier
        :param page_index: index of the page we want
        :param page_size: size of the page we want
        :return: a list of runs
        """
        return self._client.list_runs(job_id, page_index, page_size)

    @classmethod
    def create_dataset_version(cls, description: Optional[str] = None) -> DatasetVersionArtifact:
        """
        create an artifact that contains a version of a dataset

        :param description: description of the dataset version
        :return: a dataset version artifact
        """
        return Artifacts.create_dataset_version(description)

    @classmethod
    def create_model_version(cls, description: Optional[str] = None) -> ModelVersionArtifact:
        """
        create an artifact that contains a version of a model

        :param description: description of the model version
        :return: a model version artifact
        """
        return Artifacts.create_model_version(description)

    @classmethod
    def create_code_version(cls, path: str = ".") -> Optional[CodeVersionArtifact]:
        """
        create an artifact that contains a version of a code

        :param path: the path to the source code
        :return: a code version artifact
        """
        return Artifacts.create_code_version(path)

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
        return Artifacts.create_code_version_with_github_uri(uri, script_relative_path, login_or_token, password, jwt)

    @classmethod
    def prepare_run(cls, job_name: str, job_type: Optional[str] = None) -> RunnableJob:
        """
        create a local object of a run. Note that the run is not created in
        vectice server (and as a consequence is NOT visible).

        The returned instance need to be used with associated py:function:: Vectice.save_after_run

        See py::class::

        :param job_name: the name of the job the run is related to
        :param job_type: type of the job.
        :return: a runnable job
        """
        return create_run(job_name, job_type)

    @classmethod
    def save_after_run(
        cls,
        project_token: str,
        run: Any,
        lib: Optional[str],
        inputs: Optional[List[Artifact]] = None,
        outputs: Optional[List[Artifact]] = None,
    ) -> Optional[int]:
        """
        save all run information in vectice server.

        :param project_token: the token of the project the job is belong to
        :param run: the run we want to save
        :param lib: Name of the lib you are using (for now, None or MLFlow)
        :param inputs: list of inputs (artifact) you are using in this run
        :param outputs: list of outputs (artifact) you are using in this run
        :return: id of the saved run or None if the run can not be saved
        """
        return save_after_run(project_token, run, lib, inputs, outputs)
