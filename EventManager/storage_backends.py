import requests
from django.core.files.storage import Storage
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class SupabaseStorage(Storage):
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.bucket = settings.SUPABASE_BUCKET
        if not all([self.url, self.key, self.bucket]):
            raise ImproperlyConfigured("Supabase storage is not properly configured")

    def _save(self, name, content):
        path = f"{self.bucket}/{name}"
        files = {'file': (name, content.read())}
        response = requests.post(
            f"{self.url}/storage/v1/object/{path}",
            files=files,
            headers={"apikey": self.key, "Authorization": f"Bearer {self.key}"}
        )
        response.raise_for_status()
        return path

    def url(self, name):
        return f"{self.url}/storage/v1/object/public/{self.bucket}/{name}"

    def delete(self, name):
        path = f"{self.bucket}/{name}"
        response = requests.delete(
            f"{self.url}/storage/v1/object/{path}",
            headers={"apikey": self.key, "Authorization": f"Bearer {self.key}"}
        )
        response.raise_for_status()
