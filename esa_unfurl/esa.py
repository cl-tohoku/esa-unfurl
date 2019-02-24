from dataclasses import dataclass
from typing import Tuple
from urllib.parse import urlparse

import requests


def parse_url(url: str) -> Tuple[str, int]:
    o = urlparse(url)
    return o.netloc.split(".")[0], int(o.path.split("/")[-1])


def truncate_text(text: str) -> str:
    lines = text.split("\n")
    n_chars = 0
    truncated_lines = []
    for line in lines:
        if n_chars > 400:
            break
        n_chars += len(line)
        truncated_lines.append(line)
    return "\n".join(truncated_lines)


@dataclass
class EsaPage:
    title: str
    url: str
    text: str

    @classmethod
    def request(cls, url: str, token: str) -> "EsaPage":
        team_name, post_number = parse_url(url)
        api_url = f"https://api.esa.io/v1/teams/{team_name}/posts/{post_number}"
        headers = {"Authorization": f"Bearer {token}"}

        r = requests.get(api_url, headers=headers)
        data = r.json()
        title = data["full_name"]
        text = data["body_md"]

        return cls(title, url, text)

    def to_attachment(self):
        return {
            "title": self.title,
            "title_link": self.url,
            "color": "#0a9b94",
            "text": truncate_text(self.text),
            "footer_icon": "esa",
            "footer": "https://assets.esa.io/assets/favicon-645bbf85cffa3c60eda21ee9cf63ff12d6f41814353dd3d4ce1a10479d795d71.ico",
        }
