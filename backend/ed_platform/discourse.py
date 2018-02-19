import json
import logging

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from ed_platform import RestException


class Discourse:

    logger = logging.getLogger("Discourse")

    def __init__(self, app):
        self.url = app.config['DISCOURSE']['url']
        self.key = app.config['DISCOURSE']['key']
        self.user = app.config['DISCOURSE']['user']
        self.workshop_link = app.config['DISCOURSE']['workshop_link']
        try:
            self.category = self.createCategory(app.config['DISCOURSE_CATEGORY'])
            self.group = self.createGroup(app.config['DISCOURSE_USER_GROUP'])
        except:
            print("Error encountered connecting to Discourse, these features may not work correctly.")


    def headers(self):
        return {
            "Content-Type": "application/json"
        }

    def urlForTopic(self, topic_id):
        return "%s/t/%i" % (self.url, topic_id)

    def createTopic(self, workshop):
        '''Creates a new topic, and makes it owned by the workshop instructor.'''
        discourse_account = self.getAccount(workshop.instructor)
        if(not discourse_account):
            self.createAccount(workshop.instructor)
            discourse_account = self.getAccount(workshop.instructor)

        link = "[%s](%s/%i)" % ("Sign up on Cadre Academy",
                             self.workshop_link, workshop.id)

        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": discourse_account.username,
                "category": str(self.category.id),
                "title": "%s with %s (CA Workshop #%i)" % (workshop.title, workshop.instructor.display_name, workshop.id),
                "raw": "%s\n%s" % (link, workshop.description)
            }
        )
        url = "%s/posts" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})

        print(response.json())
        if(response.status_code < 200 or response.status_code > 299):
            raise RestException({'code': 'topic_creation_failed', 'message': json.dumps(response.json())})
        try:
            return Topic(response.json())
        except:
            raise RestException({'code':'topic_creation_failed', 'message':json.dumps(response.json())})

    def createPost(self, workshop, participant, message):
        discourse_account = self.getAccount(participant)
        if(not discourse_account):
            self.createAccount(participant)
            discourse_account = self.getAccount(participant)
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": discourse_account.username,
                "topic_id": str(workshop.discourse_topic_id),
                "raw": message
            }
        )
        url = "%s/posts" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})

        print(response.json())
        response.raise_for_status()
        return Topic(response.json())

    def getTopic(self, workshop):
        url = "%s/t/%i.json?api_key=%s&api_username=%s" % (self.url, workshop.discourse_topic_id, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        return Topic(response.json())

    def deleteTopic(self, id):
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
            }
        )
        url = "%s/t/%i.json" % (self.url, id)

        response = requests.delete(url, data=multipart_data,
                                   headers={'Content-Type': multipart_data.content_type})


    def createAccount(self, participant):
        """Returns the user id, if successful"""
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
                "name": participant.display_name,
                "email": participant.email_address,
                "password": "1LousyPassPhrase!",
                "username": participant.uid,
                "group": str(self.group.id),
                "active": "True",
                "approved": "True"
            }
        )
        url = "%s/users.json" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()
        user_id = response.json()["user_id"]
        self.addUserToGroup(user_id, self.group.id)
        return user_id

    def addUserToGroup(self, user_id, group_id):
        """Returns the user id, if successful"""
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
                "group_id": str(group_id),
            }
        )
        url = "%s/admin/users/%i/groups" % (self.url, user_id)
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()


    def getAccount(self, participant):
        """Returns None if the user does not exist."""
        discourseAccount = self._searchAccounts(participant.email_address)
        if discourseAccount == None:
            discourseAccount = self._searchAccounts(participant.uid)
        return discourseAccount

    def _searchAccounts(self, query):
        url = "%s/admin/users/list/all.json?api_key=%s&api_username=%s&filter=%s" % (self.url, self.key, self.user, query)
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        if(len(json) > 0 and "id" in json[0]): return DiscourseAccount(json[0]);

    def deleteAccount(self, account):
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
            }
        )
        url = "%s/admin/users/%i.json" % (self.url, account.id)

        response = requests.delete(url, data=multipart_data,
                                   headers={'Content-Type': multipart_data.content_type})


    def getCategories(self):
        url = "%s/categories.json?api_key=%s&api_username=%s" % (self.url, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        categories = []
        for cat in response.json()['category_list']['categories']:
            categories.append(Category(cat))
        return categories

    def createCategory(self, name):
        """Returns the category if it exists already, or can be created"""
        for cat in self.getCategories():
            print(cat.name)
            if(cat.name == name):
                print("Found Category:" + str(cat))
                return cat
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
                "name": name,
                "color": "E67116",
                "text_color": "000000"
            }
        )
        url = "%s/categories" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()
        print("Created Category:" + str(response.json()))
        return Category(response.json()['category'])

    def deletePostsInCategory(self):
        """Returns None if the user does not exist."""
        url = "%s/c/%i.json?api_key=%s&api_username=%s" % (self.url, self.category.id, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        for topic in json['topic_list']['topics']:
            self.delete_topic(topic["id"])

    def getGroups(self):
        url = "%s/admin/groups.json?api_key=%s&api_username=%s" % (self.url, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        groups = []
        for group in response.json():
            groups.append(Group(group))
        return groups

    def createGroup(self, name):
        '''Creates a new group for adding new users.  Sets the trust level to 1, so these
        users are not considered "New Users", so we are not approving their message posts.'''
        for group in self.getGroups():
            if(group.name == name):
                return group
        """Returns the user id, if successful"""
        multipart_data = MultipartEncoder(
            fields={
                "api_key": self.key,
                "api_username": self.user,
                "group[name]": name,
                "group[grant_trust_level]": "2"
            }
        )
        url = "%s/admin/groups" % self.url
        response = requests.post(url, data=multipart_data,
                                 headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()
        print("Create Group:" + str(response.json()))
        return Group(response.json()['basic_group'])

    def deleteUsersAndPostsByGroup(self):
        """Deletes all the posts created by users in the default group, useful to cleaning up after testing.
           I wanted to Delete the users as well, but this just times out for some reason, so giving up on that."""
        url = "%s/groups/%s/members.json?api_key=%s&api_username=%s" % (self.url, self.group.name, self.key, self.user)
        response = requests.get(url)
        response.raise_for_status()
        members = response.json()["members"]
        for member in members:
            url = "%s/admin/users/%i/delete_all_posts?api_key=%s&api_username=%s" % (self.url, member["id"], self.key, self.user)
            response = requests.put(url)
            response.raise_for_status()
            url = "%s/admin/users/%i?api_key=%s&api_username=%s" % (self.url, member["id"], self.key, self.user)
            response = requests.delete(url)
            response.raise_for_status()


class Topic:

    logger = logging.getLogger("Discourse.Topic")
    cooked = ""
    participant = None

    def __init__(self,rv):
        self.id = rv["id"]
        if("topic_id" in rv): self.id = rv["topic_id"]
        self.deleted = rv["deleted_at"] is not None
        self.user_id = rv["user_id"]
        if("posts_count" in rv): self.posts_count = rv["posts_count"]
        if("created_at" in rv): self.created_at = rv["created_at"]
        if "display_username" in rv: self.display_username = rv["display_username"]
        if "username" in rv: self.uid = rv["username"]
        if "cooked" in rv: self.cooked = rv["cooked"]
        self.posts = []
        if "post_stream" in rv:
            for post in rv['post_stream']['posts']:
                if post["post_number"] != 1:
                    self.posts.append(Topic(post))

    def toJSON(self):
        topic_json = json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)

        return topic_json

class DiscourseAccount:
    logger = logging.getLogger("Discourse.Topic")

    def __init__(self,rv):
        self.id = rv["id"]
        self.username = rv["username"]
        self.active = rv["active"]
        self.admin = rv["admin"]
        self.moderator = rv["moderator"]

class Category:
    def __init__(self,rv):
        self.id = rv["id"]
        self.name = rv["name"]
        self.description = rv["description"]

class Group:
    def __init__(self,rv):
        self.id = rv["id"]
        self.name = rv["name"]
        self.user_count = rv["user_count"]