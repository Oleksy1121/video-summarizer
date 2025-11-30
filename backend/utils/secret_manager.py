from google.cloud import secretmanager
import tempfile
import logging

def get_secret_file_path(project_id: str, secret_id: str) -> str:
    """
    Pobiera sekret z GCP Secret Manager i zapisuje tymczasowo do pliku.
    Zwraca ścieżkę do pliku.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        secret_content = response.payload.data.decode("UTF-8")

        # Zapis do tymczasowego pliku
        tmp_file = tempfile.NamedTemporaryFile(delete=False, mode="w")
        tmp_file.write(secret_content)
        tmp_file.close()
        logging.info(f"Secret {secret_id} fetched and saved to temporary file: {tmp_file.name}")
        return tmp_file.name

    except Exception as e:
        logging.exception(f"Failed to fetch secret {secret_id}: {e}")
        return None