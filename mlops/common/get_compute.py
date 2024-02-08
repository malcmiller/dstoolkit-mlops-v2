"""
This module provides functionality for managing Azure Machine Learning compute resources.

It includes functions to get an existing compute target or create a new one in an Azure
Machine Learning workspace. The module uses the Azure Machine Learning SDK for Python to
interact with Azure resources. It is designed to be run as a standalone script with command-line
arguments for specifying the details of the Azure Machine Learning compute target.
"""

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import argparse
from azure.ai.ml.entities import AmlCompute


def get_compute(
    subscription_id: str,
    resource_group_name: str,
    workspace_name: str,
    cluster_name: str,
    cluster_size: str,
    cluster_region: str,
    min_instances: int = 0,
    max_instances: int = 4,
    idle_time_before_scale_down: int = 600,
):
    """Get an existing compute or create a new one."""
    compute_object = None
    try:
        client = MLClient(
            DefaultAzureCredential(),
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            workspace_name=workspace_name,
        )
        try:
            compute_object = client.compute.get(cluster_name)
            print(f"Found existing compute target {cluster_name}, so using it.")
        except Exception:
            print(f"{cluster_name} is not found! Trying to create a new one.")
            compute_object = AmlCompute(
                name=cluster_name,
                type="amlcompute",
                size=cluster_size,
                location=cluster_region,
                min_instances=min_instances,
                max_instances=max_instances,
                idle_time_before_scale_down=idle_time_before_scale_down,
            )
            compute_object = client.compute.begin_create_or_update(
                compute_object
            ).result()
            print(f"A new cluster {cluster_name} has been created.")
    except Exception as ex:
        print("Oops!  invalid credentials.. Try again...", ex)
        raise
    return compute_object


def main():
    """Take command line parameters and returns a reference to the compute."""
    parser = argparse.ArgumentParser("get_compute")
    parser.add_argument("--subscription_id", type=str, help="Azure subscription id")
    parser.add_argument(
        "--resource_group_name", type=str, help="Azure Machine learning resource group"
    )
    parser.add_argument(
        "--workspace_name", type=str, help="Azure Machine learning Workspace name"
    )
    parser.add_argument(
        "--cluster_name", type=str, help="Azure Machine learning cluster name"
    )
    parser.add_argument(
        "--cluster_size", type=str, help="Azure Machine learning cluster size"
    )
    parser.add_argument(
        "--cluster_region", type=str, help="Azure Machine learning cluster region"
    )
    parser.add_argument("--min_instances", type=int, default=0)
    parser.add_argument("--max_instances", type=int, default=4)
    parser.add_argument("--idle_time_before_scale_down", type=int, default=1800)

    args = parser.parse_args()
    get_compute(
        args.subscription_id,
        args.resource_group_name,
        args.workspace_name,
        args.cluster_name,
        args.cluster_size,
        args.cluster_region,
        args.min_instances,
        args.max_instances,
        args.idle_time_before_scale_down,
    )


if __name__ == "__main__":
    main()
