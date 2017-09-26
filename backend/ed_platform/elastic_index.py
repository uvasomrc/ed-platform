from flask import logging

from elasticsearch_dsl import DocType, Date, Float, Keyword, Text, \
    Index, analyzer, Nested, Integer, analysis
from elasticsearch import Elasticsearch
import elasticsearch
import elasticsearch_dsl
from elasticsearch.helpers import scan
from elasticsearch_dsl.connections import connections
import os
import logging


class ElasticIndex:

    logger = logging.getLogger("ElasticIndex")

    def __init__(self, app):
        self.logger.debug("Initializing Elastic Idnex")
        self.establish_connection(app.config['ELASTIC_SEARCH'])
        self.index_name = app.config['ELASTIC_SEARCH']["index_name"]
        self.index = Index(self.index_name)
        self.index.doc_type(ElasticWorkshop)
        try:
            ElasticWorkshop.init()
        except:
            self.logger.info("Failed to create the workshop index.  It may already exist.")


    def establish_connection(self, settings):
        """Establish connection to an ElasticSearch host, and initialize the Submission collection"""
        self.conenction = connections.create_connection(hosts=settings["hosts"],
                                                        port=settings["port"],
                                                        timeout=settings["timeout"],
                                                        verify_certs=settings["verify_certs"],
                                                        use_ssl=settings["use_ssl"],
                                                        http_auth=(settings["http_auth_user"],
                                                                   settings["http_auth_pass"]))

    def clear(self):
        try:
            self.logger.info("Clearing the index.")
            self.index.delete(ignore=404)
        except:
            self.logger.error("Failed to delete the workshop index.  It night not exist.")

    def load_all(self, workshops):
        for w in workshops:

            for s in w.sessions:
                ew = ElasticWorkshop(id=w.id,
                                     title=w.title,
                                     description=w.description,
                                     date=s.date_time,
                                     location=s.location,
                                     open=s.open(),
                                     notes=s.instructor_notes
                                     )
                ElasticWorkshop.save(ew)


class ElasticWorkshop(DocType):
    """A flattened version of the index where Title, SelfText, and Comment Text are all top level documents"""
    id = Keyword()
    title = Text()
    description = Text()
    date = Date()
    location = Keyword()
    open = Keyword()
    notes = Text()
    messages = Text()
