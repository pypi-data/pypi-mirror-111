"""
Type annotations for ecs service client paginators.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_ecs import ECSClient
    from mypy_boto3_ecs.paginator import (
        ListAccountSettingsPaginator,
        ListAttributesPaginator,
        ListClustersPaginator,
        ListContainerInstancesPaginator,
        ListServicesPaginator,
        ListTaskDefinitionFamiliesPaginator,
        ListTaskDefinitionsPaginator,
        ListTasksPaginator,
    )

    client: ECSClient = boto3.client("ecs")

    list_account_settings_paginator: ListAccountSettingsPaginator = client.get_paginator("list_account_settings")
    list_attributes_paginator: ListAttributesPaginator = client.get_paginator("list_attributes")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_container_instances_paginator: ListContainerInstancesPaginator = client.get_paginator("list_container_instances")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_task_definition_families_paginator: ListTaskDefinitionFamiliesPaginator = client.get_paginator("list_task_definition_families")
    list_task_definitions_paginator: ListTaskDefinitionsPaginator = client.get_paginator("list_task_definitions")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""
import sys
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from .literals import (
    ContainerInstanceStatusType,
    DesiredStatusType,
    LaunchTypeType,
    SchedulingStrategyType,
    SettingNameType,
    SortOrderType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
)
from .type_defs import (
    ListAccountSettingsResponseResponseTypeDef,
    ListAttributesResponseResponseTypeDef,
    ListClustersResponseResponseTypeDef,
    ListContainerInstancesResponseResponseTypeDef,
    ListServicesResponseResponseTypeDef,
    ListTaskDefinitionFamiliesResponseResponseTypeDef,
    ListTaskDefinitionsResponseResponseTypeDef,
    ListTasksResponseResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListAccountSettingsPaginator",
    "ListAttributesPaginator",
    "ListClustersPaginator",
    "ListContainerInstancesPaginator",
    "ListServicesPaginator",
    "ListTaskDefinitionFamiliesPaginator",
    "ListTaskDefinitionsPaginator",
    "ListTasksPaginator",
)


class ListAccountSettingsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListAccountSettings)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listaccountsettingspaginator)
    """

    def paginate(
        self,
        *,
        name: SettingNameType = None,
        value: str = None,
        principalArn: str = None,
        effectiveSettings: bool = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAccountSettingsResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListAccountSettings.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listaccountsettingspaginator)
        """


class ListAttributesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListAttributes)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listattributespaginator)
    """

    def paginate(
        self,
        *,
        targetType: Literal["container-instance"],
        cluster: str = None,
        attributeName: str = None,
        attributeValue: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListAttributesResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListAttributes.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listattributespaginator)
        """


class ListClustersPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListClusters)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listclusterspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListClustersResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListClusters.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listclusterspaginator)
        """


class ListContainerInstancesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListContainerInstances)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listcontainerinstancespaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = None,
        filter: str = None,
        status: ContainerInstanceStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListContainerInstancesResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListContainerInstances.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listcontainerinstancespaginator)
        """


class ListServicesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListServices)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listservicespaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = None,
        launchType: LaunchTypeType = None,
        schedulingStrategy: SchedulingStrategyType = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListServicesResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listservicespaginator)
        """


class ListTaskDefinitionFamiliesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitionFamilies)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskdefinitionfamiliespaginator)
    """

    def paginate(
        self,
        *,
        familyPrefix: str = None,
        status: TaskDefinitionFamilyStatusType = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTaskDefinitionFamiliesResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitionFamilies.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskdefinitionfamiliespaginator)
        """


class ListTaskDefinitionsPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitions)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskdefinitionspaginator)
    """

    def paginate(
        self,
        *,
        familyPrefix: str = None,
        status: TaskDefinitionStatusType = None,
        sort: SortOrderType = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTaskDefinitionsResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTaskDefinitions.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskdefinitionspaginator)
        """


class ListTasksPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTasks)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskspaginator)
    """

    def paginate(
        self,
        *,
        cluster: str = None,
        containerInstance: str = None,
        family: str = None,
        startedBy: str = None,
        serviceName: str = None,
        desiredStatus: DesiredStatusType = None,
        launchType: LaunchTypeType = None,
        PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTasksResponseResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.101/reference/services/ecs.html#ECS.Paginator.ListTasks.paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecs/paginators.html#listtaskspaginator)
        """
