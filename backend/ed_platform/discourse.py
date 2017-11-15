import logging

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class Discourse:

    logger = logging.getLogger("Discourse")

    def __init__(self, app):
        self.url = app.config['DISCOURSE']['url']
        self.key = app.config['DISCOURSE']['key']
        self.user = app.config['DISCOURSE']['user']
        pass

    def headers(self):
        return {
            "Content-Type": "application/json"
        }

    def get_posts(self):
        url = "%s/%s?api_key=%s&api_username=%s" % (self.url, "posts.json", self.key, self.user)
        response = requests.get(url, headers=self.headers())
        response.raise_for_status()
        print(response.json())

    def url_for_topic(self, topic_id):
        return "%s/t/%i" % (self.url, topic_id)

    def create_topic(self, workshop):
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
                "category": "workshop",
                "title": workshop.title,
                "raw": workshop.description
            }
        )
        url = "%s/posts" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})

        print(response.json())
        response.raise_for_status()
        return Topic(response.json())

    def get_topic(self, id):
        url = "%s/t/%i.json?api_key=%s&api_username=%s" % (self.url, id, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        return Topic(response.json())

    def delete_topic(self, id):
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
            }
        )
        url = "%s/t/%i.json" % (self.url, id)

        response = requests.delete(url, data=multipart_data,
                                   headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()

class Topic:

    logger = logging.getLogger("Discourse.Topic")

    def __init__(self,rv):
        self.id = rv["id"]
        if("topic_id" in rv):
            self.id = rv["topic_id"]
        self.deleted = rv["deleted_at"] is not None


