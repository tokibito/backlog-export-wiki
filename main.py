import os

from dotenv import dotenv_values
import httpx

"""
requirements:
- python-dotenv
- httpx
"""

config = {
    **dotenv_values(".env"),
    **os.environ,
}

BACKLOG_DOMAIN = config.get("BACKLOG_DOMAIN")
BACKLOG_API_KEY = config.get("BACKLOG_API_KEY")
BACKLOG_PROJECT_KEY = config.get("BACKLOG_PROJECT_KEY")


class BacklogWikiExport:
    def __init__(self, domain, api_key, project_key):
        self.domain = domain
        self.api_key = api_key
        self.project_key = project_key

    def run(self):
        wiki_pages = self.list_wiki_pages()
        for wiki_page_meta in wiki_pages:
            wiki_id = wiki_page_meta["id"]
            name = (
                wiki_page_meta["name"]
                .replace("/", "_")
                .replace(" ", "_")
                .replace(".", "_")
            )
            wiki_page = self.fetch_wiki_page(wiki_id)
            filename = f"{self.project_key}-{wiki_id}-{name}.md"
            print(f"writing {filename}")
            with open(filename, "w") as fp:
                fp.write(wiki_page["content"] or "")

    def list_wiki_pages(self):
        response = httpx.get(
            f"https://{self.domain}/api/v2/wikis?apiKey={self.api_key}&projectIdOrKey={self.project_key}"
        )
        return response.json()

    def fetch_wiki_page(self, wiki_id):
        response = httpx.get(
            f"https://{self.domain}/api/v2/wikis/{wiki_id}?apiKey={self.api_key}"
        )
        return response.json()


def main():
    app = BacklogWikiExport(
        domain=BACKLOG_DOMAIN, api_key=BACKLOG_API_KEY, project_key=BACKLOG_PROJECT_KEY
    )
    app.run()


if __name__ == "__main__":
    main()
