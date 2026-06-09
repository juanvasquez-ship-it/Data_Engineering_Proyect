from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
import logging
import os

log = logging.getLogger("airflow.task")


def upload_to_adls(
    local_file_path="/opt/airflow/data/sample.txt",
    container_name="airflow",
    blob_name="raw/uploaded_sample.txt",
    wasb_conn_id="azure_blob_storage"
):
    try:
        if not os.path.exists(local_file_path):
            log.warning(f"==> Local file not found: {local_file_path}")
            raise FileNotFoundError(f"No existe el archivo local: {local_file_path}")

        hook = WasbHook(wasb_conn_id=wasb_conn_id)

        hook.load_file(
            file_path=local_file_path,
            container_name=container_name,
            blob_name=blob_name,
            overwrite=True
        )

        existe = hook.check_for_blob(
            container_name=container_name,
            blob_name=blob_name
        )

        if existe:
            log.info("==> Archivo subido correctamente a Azure.")
            log.info(f"==> Archivo local: {local_file_path}")
            log.info(f"==> Container: {container_name}")
            log.info(f"==> Blob: {blob_name}")
        else:
            raise Exception("El archivo se intentó subir, pero no se encontró en Azure.")

    except Exception:
        log.error("==> Failed to upload to Azure Blob", exc_info=True)
        raise