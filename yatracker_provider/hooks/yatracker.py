import requests
import tenacity
from airflow.exceptions import AirflowNotFoundException
from airflow.hooks.base import BaseHook

from ..models.issue import (
    IssueImport,
    IssueImported,
    IssueLink,
    IssueModel,
    IssueModify,
    IssueRelationship,
    IssueSearch,
    IssueTransited,
)


class YatrackerHook(BaseHook):
    conn_name_attr = "http_conn_id"
    default_conn_name = "yatracker_default"
    conn_type = "http"
    hook_name = "YATRACKER"

    def __init__(self, yatracker_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.yatracker_conn_id = yatracker_conn_id
        self.base_url = ""
        self.token = ""
        self.org_id = ""
        self.api_ver = "v2"
        self.retry_obj = tenacity.Retrying(
            stop=tenacity.stop_after_attempt(3),
            retry=tenacity.retry_if_exception_type(
                (
                    requests.ConnectTimeout,
                    requests.HTTPError,
                )
            ),
        )

    def get_conn(self):
        session = requests.Session()
        headers = {}
        conn = self.get_connection(self.yatracker_conn_id)
        if not conn.host:
            raise AirflowNotFoundException("Host not provided in configuration")
        self.base_url = conn.host
        if not conn.login:
            raise AirflowNotFoundException(f"Connection to {conn.host} requires login ")
        headers["Authorization"] = f"OAuth {conn.login}"
        if not conn.password:
            raise AirflowNotFoundException(
                f"Connection to {conn.host} requires password"
            )
        headers["X-Org-Id"] = conn.password
        session.headers.update(headers)
        return session

    def __import_issue(self, data: IssueImport) -> IssueImported:
        session = self.get_conn()
        url = f"{self.base_url}/{self.api_ver}/issues/_import"
        r = session.post(url=url, data=data.json(by_alias=True, exclude_none=True))
        r.raise_for_status()
        payload = r.json()
        session.close()
        return IssueImported.parse_obj(payload)

    def import_issue(self, data: IssueImport) -> IssueImported:
        return self.retry_obj(self.__import_issue, data)

    def __edit_issue(self, issue_id: str, data: IssueModify) -> IssueModel:
        session = self.get_conn()
        url = f"{self.base_url}/{self.api_ver}/issues/{issue_id}"
        r = session.patch(url=url, data=data.json(by_alias=True, exclude_none=True))
        r.raise_for_status()
        payload = r.json()
        session.close()
        return IssueModel.parse_obj(payload)

    def edit_issue(self, issue_id: str, data: IssueModify) -> IssueModel:
        return self.retry_obj(self.__edit_issue, issue_id, data)

    def __link_issues(self, issue_id: str, data: IssueLink) -> IssueRelationship:
        session = self.get_conn()
        url = f"{self.base_url}/{self.api_ver}/issues/{issue_id}/links"
        r = session.post(url=url, data=data.json(by_alias=True, exclude_none=True))
        r.raise_for_status()
        payload = r.json()
        return IssueRelationship.parse_obj(payload)

    def link_issues(self, issue_id: str, data: IssueLink) -> IssueRelationship:
        return self.retry_obj(self.__link_issues, issue_id, data)

    def __transit_issue(self, issue_id: str, transition_id: int) -> IssueTransited:
        session = self.get_conn()
        url = f"{self.base_url}/{self.api_ver}/issues/{issue_id}/transitions/{transition_id}/_execute"
        r = session.post(url=url)
        r.raise_for_status()
        payload = r.json()
        return IssueTransited.parse_obj(payload)

    def transit_issues(self, issue_id: str, transition_id: int) -> IssueTransited:
        return self.retry_obj(self.__transit_issue, issue_id, transition_id)

    def __search_issue(self, data: IssueSearch) -> IssueModel:
        session = self.get_conn()
        url = f"{self.base_url}/{self.api_ver}/issues/_search"
        r = session.post(url=url, data=data.json(by_alias=True, exclude_none=True))
        r.raise_for_status()
        payload = r.json()
        return IssueModel.parse_obj(payload)

    def search_issue(self, data: IssueSearch) -> IssueModel:
        return self.retry_obj(self.__search_issue, data)

    def run(self):
        raise NotImplementedError
