"""
Type annotations for support service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_support import SupportClient

    client: SupportClient = boto3.client("support")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator
from .type_defs import (
    AddAttachmentsToSetResponseResponseTypeDef,
    AddCommunicationToCaseResponseResponseTypeDef,
    AttachmentTypeDef,
    CreateCaseResponseResponseTypeDef,
    DescribeAttachmentResponseResponseTypeDef,
    DescribeCasesResponseResponseTypeDef,
    DescribeCommunicationsResponseResponseTypeDef,
    DescribeServicesResponseResponseTypeDef,
    DescribeSeverityLevelsResponseResponseTypeDef,
    DescribeTrustedAdvisorCheckRefreshStatusesResponseResponseTypeDef,
    DescribeTrustedAdvisorCheckResultResponseResponseTypeDef,
    DescribeTrustedAdvisorChecksResponseResponseTypeDef,
    DescribeTrustedAdvisorCheckSummariesResponseResponseTypeDef,
    RefreshTrustedAdvisorCheckResponseResponseTypeDef,
    ResolveCaseResponseResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SupportClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AttachmentIdNotFound: Type[BotocoreClientError]
    AttachmentLimitExceeded: Type[BotocoreClientError]
    AttachmentSetExpired: Type[BotocoreClientError]
    AttachmentSetIdNotFound: Type[BotocoreClientError]
    AttachmentSetSizeLimitExceeded: Type[BotocoreClientError]
    CaseCreationLimitExceeded: Type[BotocoreClientError]
    CaseIdNotFound: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DescribeAttachmentLimitExceeded: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]


class SupportClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def add_attachments_to_set(
        self, *, attachments: List["AttachmentTypeDef"], attachmentSetId: str = None
    ) -> AddAttachmentsToSetResponseResponseTypeDef:
        """
        Adds one or more attachments to an attachment set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.add_attachments_to_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#add_attachments_to_set)
        """

    def add_communication_to_case(
        self,
        *,
        communicationBody: str,
        caseId: str = None,
        ccEmailAddresses: List[str] = None,
        attachmentSetId: str = None
    ) -> AddCommunicationToCaseResponseResponseTypeDef:
        """
        Adds additional customer communication to an AWS Support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.add_communication_to_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#add_communication_to_case)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#can_paginate)
        """

    def create_case(
        self,
        *,
        subject: str,
        communicationBody: str,
        serviceCode: str = None,
        severityCode: str = None,
        categoryCode: str = None,
        ccEmailAddresses: List[str] = None,
        language: str = None,
        issueType: str = None,
        attachmentSetId: str = None
    ) -> CreateCaseResponseResponseTypeDef:
        """
        Creates a case in the AWS Support Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.create_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#create_case)
        """

    def describe_attachment(
        self, *, attachmentId: str
    ) -> DescribeAttachmentResponseResponseTypeDef:
        """
        Returns the attachment that has the specified ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_attachment)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_attachment)
        """

    def describe_cases(
        self,
        *,
        caseIdList: List[str] = None,
        displayId: str = None,
        afterTime: str = None,
        beforeTime: str = None,
        includeResolvedCases: bool = None,
        nextToken: str = None,
        maxResults: int = None,
        language: str = None,
        includeCommunications: bool = None
    ) -> DescribeCasesResponseResponseTypeDef:
        """
        Returns a list of cases that you specify by passing one or more case IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_cases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_cases)
        """

    def describe_communications(
        self,
        *,
        caseId: str,
        beforeTime: str = None,
        afterTime: str = None,
        nextToken: str = None,
        maxResults: int = None
    ) -> DescribeCommunicationsResponseResponseTypeDef:
        """
        Returns communications and attachments for one or more support cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_communications)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_communications)
        """

    def describe_services(
        self, *, serviceCodeList: List[str] = None, language: str = None
    ) -> DescribeServicesResponseResponseTypeDef:
        """
        Returns the current list of AWS services and a list of service categories for
        each service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_services)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_services)
        """

    def describe_severity_levels(
        self, *, language: str = None
    ) -> DescribeSeverityLevelsResponseResponseTypeDef:
        """
        Returns the list of severity levels that you can assign to a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_severity_levels)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_severity_levels)
        """

    def describe_trusted_advisor_check_refresh_statuses(
        self, *, checkIds: List[str]
    ) -> DescribeTrustedAdvisorCheckRefreshStatusesResponseResponseTypeDef:
        """
        Returns the refresh status of the AWS Trusted Advisor checks that have the
        specified check IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_trusted_advisor_check_refresh_statuses)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_trusted_advisor_check_refresh_statuses)
        """

    def describe_trusted_advisor_check_result(
        self, *, checkId: str, language: str = None
    ) -> DescribeTrustedAdvisorCheckResultResponseResponseTypeDef:
        """
        Returns the results of the AWS Trusted Advisor check that has the specified
        check ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_trusted_advisor_check_result)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_trusted_advisor_check_result)
        """

    def describe_trusted_advisor_check_summaries(
        self, *, checkIds: List[str]
    ) -> DescribeTrustedAdvisorCheckSummariesResponseResponseTypeDef:
        """
        Returns the results for the AWS Trusted Advisor check summaries for the check
        IDs that you specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_trusted_advisor_check_summaries)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_trusted_advisor_check_summaries)
        """

    def describe_trusted_advisor_checks(
        self, *, language: str
    ) -> DescribeTrustedAdvisorChecksResponseResponseTypeDef:
        """
        Returns information about all available AWS Trusted Advisor checks, including
        the name, ID, category, description, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.describe_trusted_advisor_checks)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#describe_trusted_advisor_checks)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#generate_presigned_url)
        """

    def refresh_trusted_advisor_check(
        self, *, checkId: str
    ) -> RefreshTrustedAdvisorCheckResponseResponseTypeDef:
        """
        Refreshes the AWS Trusted Advisor check that you specify using the check ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.refresh_trusted_advisor_check)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#refresh_trusted_advisor_check)
        """

    def resolve_case(self, *, caseId: str = None) -> ResolveCaseResponseResponseTypeDef:
        """
        Resolves a support case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Client.resolve_case)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/client.html#resolve_case)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_cases"]) -> DescribeCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Paginator.DescribeCases)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/paginators.html#describecasespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_communications"]
    ) -> DescribeCommunicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/support.html#Support.Paginator.DescribeCommunications)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_support/paginators.html#describecommunicationspaginator)
        """
