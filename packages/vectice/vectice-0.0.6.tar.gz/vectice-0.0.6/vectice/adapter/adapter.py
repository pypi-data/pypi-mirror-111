from __future__ import annotations

import logging
from abc import abstractmethod, ABC
from typing import List, Optional, Any, Dict

from vectice.api import Client
from vectice.api.json_object import JsonObject
from vectice.models import Artifact, Job, JobRun, RunnableJob, ArtifactType, CodeVersionArtifact, JobRunStatus


class AbstractAdapter(ABC):
    @property
    @abstractmethod
    def active_runs(self) -> Dict[int, ActiveRun]:
        pass

    @abstractmethod
    def create_run(self, name: str) -> RunnableJob:
        pass

    @abstractmethod
    def end_run(
        self, run: ActiveRun, outputs: Optional[List[Artifact]] = None, status: str = JobRunStatus.COMPLETED
    ) -> Optional[int]:
        pass

    @abstractmethod
    def start_run(self, run: RunnableJob, inputs: Optional[List[Artifact]] = None) -> ActiveRun:
        pass

    @abstractmethod
    def save_job_and_associated_runs(self, name: str) -> None:
        pass

    @abstractmethod
    def save_run(
        self,
        run: Any,
        inputs: Optional[List[Artifact]] = None,
        outputs: Optional[List[Artifact]] = None,
    ) -> Optional[int]:
        pass


class ActiveRun:
    """Wrapper around dict response to enable using Python ``with`` syntax."""

    _outputs: Optional[List[Artifact]]
    _adapter: AbstractAdapter
    _job: JsonObject
    _run: JsonObject
    _inputs: JsonObject

    def __init__(self, job: JsonObject, run: JsonObject, inputs: JsonObject, adapter: AbstractAdapter):
        self._adapter = adapter
        self._job = job
        self._run = run
        self._inputs = inputs
        self._outputs = None

    def __enter__(self) -> ActiveRun:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        status = JobRunStatus.COMPLETED if exc_type is None else JobRunStatus.FAILED
        self._adapter.end_run(self, status=status)
        return exc_type is None

    @property
    def outputs(self) -> Optional[List[Artifact]]:
        return self._outputs

    @property
    def run(self) -> JsonObject:
        return self._run

    @property
    def job(self) -> JsonObject:
        return self._job

    def add_output(self, output: Artifact):
        if self._outputs is None:
            self._outputs = []
        self._outputs.append(output)

    def add_outputs(self, outputs: List[Artifact]):
        if len(outputs) > 0:
            if self._outputs is None:
                self._outputs = []
            self._outputs.extend(outputs)


class Adapter(AbstractAdapter):
    def __init__(self, project_token: str, auto_connect=True):
        self._client = Client(project_token, auto_connect)
        self._active_runs: Dict[int, ActiveRun] = {}
        self._last_created_run: Optional[RunnableJob] = None
        self._last_started_run: Optional[ActiveRun] = None
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def active_runs(self) -> Dict[int, ActiveRun]:
        return self._active_runs

    def get_current_runnable_job(self, run: Optional[RunnableJob] = None) -> RunnableJob:
        if run is not None:
            result: RunnableJob = run
        else:
            if self._last_created_run is None:
                raise RuntimeError("A job context must have been created.")
            else:
                result = self._last_created_run
        return result

    def start_run(self, run: Optional[RunnableJob] = None, inputs: Optional[List[Artifact]] = None) -> ActiveRun:
        """
        start the run created before by calling create_run function

        :param run: the runnable job to start
        :param inputs: list of artifacts used as inputs by this run.
        :return: a reference to a run executing
        """

        run = self.get_current_runnable_job(run)
        code_artifact_is_present = False
        if inputs is not None:
            for an_input in inputs:
                if an_input is not None:
                    an_input.jobArtifactType = "INPUT"
                    code_artifact_is_present = code_artifact_is_present or an_input.artifactType == ArtifactType.CODE
        if not code_artifact_is_present:
            if inputs is None:
                inputs = []
            artifact = CodeVersionArtifact.create(".")
            if artifact is not None:
                inputs.append(artifact)

        response = self._client.start_run(run, inputs)
        active_run = ActiveRun(response["job"], response["jobRun"], response["jobArtifacts"], self)
        self._active_runs[active_run.run["id"]] = active_run
        self._last_started_run = active_run
        return active_run

    def _get_current_active_run(self, run: Optional[ActiveRun] = None) -> ActiveRun:
        if run is not None:
            result: ActiveRun = run
        else:
            if self._last_started_run is None:
                raise RuntimeError("A job context must have been created.")
            else:
                result = self._last_started_run
        return result

    def end_run(
        self,
        run: Optional[ActiveRun] = None,
        outputs: Optional[List[Artifact]] = None,
        status: str = JobRunStatus.COMPLETED,
    ) -> Optional[int]:
        """
        End the current (last) active run started by `start_run`.
        To end a specific run, use `stop_run` instead.

        :return: id of the run in vectice if succesfully saved
        """
        run = self._get_current_active_run(run)
        if outputs is not None:
            run.add_outputs(outputs)
        if run.outputs is not None:
            for an_output in run.outputs:
                if an_output is not None:
                    an_output.jobArtifactType = "OUTPUT"
        run.run["status"] = status
        self._client.stop_run(run.run, run.outputs)
        if "id" in run.run:
            run_id: Optional[int] = int(run.run["id"])
        else:
            run_id = None
        del self._active_runs[run.run["id"]]
        return run_id

    def __save_run(
        self,
        run: Optional[RunnableJob] = None,
        inputs: Optional[List[Artifact]] = None,
        outputs: Optional[List[Artifact]] = None,
    ) -> Optional[int]:
        if run is None:
            run = self._last_created_run
        active_run = self.start_run(run, inputs)
        return self.end_run(active_run, outputs)

    def save_job_and_associated_runs(self, name: str) -> None:
        raise RuntimeError("No implementation for this library")

    def save_run(
        self,
        run: Any,
        inputs: Optional[List[Artifact]] = None,
        outputs: Optional[List[Artifact]] = None,
    ) -> Optional[int]:
        """
        save run with its associated inputs and outputs.

        :param run: the run we want to save
        :param inputs: list of inputs (artifact) you are using in this run
        :param outputs: list of outputs (artifact) you are using in this run
        :return: id of the run in vectice if succesfully saved
        """
        if isinstance(run, RunnableJob):
            return self.__save_run(run, inputs, outputs)
        else:
            raise RuntimeError("Incompatible object provided.")

    def create_run(self, job_name: str, job_type: Optional[str] = None) -> RunnableJob:
        """
        create an instance of a future run of a job.
        the run is not started. you need to start it by calling start_run

        :param job_type: the type of job. see :class:`~vectice.models.JobType` for the list of accepted type.
        :param job_name: the name of the job that should run.
        :return: an instance of a non started run.
        """
        if job_name is None:
            raise RuntimeError("Job name must be set")
        self._last_created_run = RunnableJob(Job(job_name, job_type), JobRun())
        return self._last_created_run

    def run_failed(self, run: Optional[ActiveRun] = None):
        """
        indicate the run failed
        """
        self.__update_run_status(run, JobRunStatus.FAILED)

    def run_aborted(self, run: Optional[ActiveRun] = None):
        """
        indicate the run was aborted by the user
        """
        self.__update_run_status(run, JobRunStatus.ABORTED)

    def __update_run_status(self, active_run: Optional[ActiveRun], status: str):
        try:
            active_run = self._get_current_active_run(active_run)
            active_run.run["status"] = status
            self._client.update_run(active_run.job["id"], active_run.run["id"], active_run.run)
        except RuntimeError:
            logging.error("run failed to start.")
