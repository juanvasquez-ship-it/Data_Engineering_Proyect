from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
import logging
import os

log = logging.getLogger('airflow.task')

def upload_to_adls(local_path, container_name, blob_name):
    hook = WasbHook(wasb_conn_id="azure_blob_storage")

    hook.load_file(
        file_path=local_path,
        container_name=container_name,
        blob_name=blob_name,
        overwrite=True
    )

    existe = hook.check_for_blob(
        container_name=container_name,
        blob_name=blob_name
    )

    if existe:
        print("Archivo subido correctamente a Azure.")
        print(f"Archivo local: {local_path}")
        print(f"Container: {container_name}")
        print(f"Blob: {blob_name}")
    else:
        raise Exception("El DAG terminó, pero no se encontró el archivo en Azure.")