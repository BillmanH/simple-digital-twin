from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from datetime import UTC, datetime, timedelta
from django.conf import settings
import os 



def fetch_sas_url(blob_name):
    url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_STATIC_CONTAINER}/{blob_name}"
    sas_token = generate_blob_sas(
        account_name=settings.AZURE_ACCOUNT_NAME,
        account_key=settings.AZURE_STORAGE_KEY,
        container_name="static",
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.now(UTC) + timedelta(hours=1)
    )

    url_with_sas = f"{url}?{sas_token}"

    return url_with_sas



