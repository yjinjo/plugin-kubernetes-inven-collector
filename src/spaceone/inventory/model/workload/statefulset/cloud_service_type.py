import os

from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import (
    CardWidget,
)
from spaceone.inventory.libs.schema.metadata.dynamic_field import (
    TextDyField,
    SearchField,
    DateTimeDyField,
)
from spaceone.inventory.libs.schema.cloud_service_type import (
    CloudServiceTypeResource,
    CloudServiceTypeResponse,
    CloudServiceTypeMeta,
)

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, "widget/total_count.yml")
count_by_region_conf = os.path.join(current_dir, "widget/count_by_region.yml")
count_by_cluster_conf = os.path.join(current_dir, "widget/count_by_cluster.yml")

cst_stateful_set = CloudServiceTypeResource()
cst_stateful_set.name = "StatefulSet"
cst_stateful_set.provider = "k8s"
cst_stateful_set.group = "WorkLoad"
cst_stateful_set.service_code = "StatefulSet"
cst_stateful_set.is_primary = False
cst_stateful_set.is_major = False
cst_stateful_set.labels = ["Container"]
cst_stateful_set.tags = {
    "spaceone:icon": "https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/kubernetes/stateful_set.svg",
}

cst_stateful_set._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source("Namespace", "data.metadata.namespace"),
        TextDyField.data_source("Ready", "data.status.number_ready"),
        TextDyField.data_source("Age", "data.age"),
        TextDyField.data_source("Update Strategy", "data.spec.update_strategy.type"),
        TextDyField.data_source("Cluster", "account"),
        DateTimeDyField.data_source(
            "Start Time",
            "data.metadata.creation_timestamp",
            options={"is_optional": True},
        ),
        TextDyField.data_source("Uid", "data.uid", options={"is_optional": True}),
    ],
    search=[
        SearchField.set(name="Uid", key="data.uid"),
        SearchField.set(name="Namespace", key="data.metadata.namespace"),
        SearchField.set(name="Cluster", key="account"),
        SearchField.set(name="Number Ready", key="data.status.number_ready"),
        SearchField.set(name="Start Time", key="data.metadata.creation_timestamp"),
        SearchField.set(name="Update Strategy", key="data.spec.update_strategy.type"),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_region_conf)),
        CardWidget.set(**get_data_from_yaml(count_by_cluster_conf)),
    ],
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({"resource": cst_stateful_set}),
]
