import urllib
from pydantic import BaseModel
import settings


class MapModel(BaseModel):
    uuid: str
    name: str
    splash: str

    @property
    def splash_art_url(self):
        site = settings.SITE_URL
        url_path = urllib.parse.urljoin("/static/", self.splash)
        return urllib.parse.urljoin(site, url_path)
