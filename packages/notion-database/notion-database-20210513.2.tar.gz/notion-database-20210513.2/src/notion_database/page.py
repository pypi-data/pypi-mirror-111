from notion_database.request import Request


class Page:
    def __init__(self, integrations_token, database_id):
        self.url = 'https://api.notion.com/v1/pages'
        self.result = {}
        self.request = Request(self.url, integrations_token=integrations_token, database_id=database_id)

    def retrieve_page(self):
        pass

    def create_page(self, properties=None, children=None):
        if children is None:
            children = {}
        if properties is None:
            properties = {}
        properties = properties
        children = children
        body = {
            "parent": {
                "database_id": self.request.NOTION_DATABASE_ID
            },
            "properties": properties,
            "children": children
        }
        self.result = self.request.call_api_post(body)

    def update_page(self):
        pass
