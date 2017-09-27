from flask import logging

from elasticsearch_dsl import DocType, Date, Float, Keyword, Text, \
    Index, Search, analyzer, Nested, Integer, analysis, Q
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
        self.connection = connections.create_connection(hosts=settings["hosts"],
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
            ElasticWorkshop.init()
        except:
            self.logger.error("Failed to delete the workshop index.  It night not exist.")

    def load_all(self, workshops):
        print ("Loading workings into " + str(self.index_name))
        for w in workshops:
            ew = ElasticWorkshop(meta={'id': 'workshop_' + str(w.id)},
                                 id=w.id,
                                 title=w.title,
                                 description=w.description,
                                 )
            for s in w.sessions:
                ew.date.append(s.date_time)
                ew.location.append(s.location)
                ew.open.append(s.open()),
                ew.notes.append(s.instructor_notes)
                for email in s.email_messages:
                    ew.messages.append(email.content)
                    ew.messages.append(email.subject)
                for instructor in s.instructors():
                    ew.instructors.append(instructor.display_name)

            ElasticWorkshop.save(ew)
        self.index.flush()

    def search(self, search):
        # when using:
        #        workshop_search = BlogSearch("web framework", filters={"category": "python"})
        workshop_search = WorkshopSearch(search.query, search.filters, index=self.index_name)
        workshop_search.index = self.index_name

        return workshop_search.execute()


class ElasticWorkshop(DocType):
    """A flattened version of the index where Title, SelfText, and Comment Text are all top level documents"""
    id = Integer()
    title = Text()
    description = Text()
    date = Date(multi=True)
    location = Keyword(multi=True)
    open = Keyword(multi=True)
    notes = Text(multi=True)
    messages = Text(multi=True)
    instructors = Keyword(multi=True)
    track = Keyword(multi=True)

class WorkshopSearch(elasticsearch_dsl.FacetedSearch):

    def __init__(self, *args, **kwargs):
        self.index = kwargs["index"]
        kwargs.pop("index")
        super(WorkshopSearch, self).__init__(*args, **kwargs)


    doc_types = [ElasticWorkshop]
    fields = ['title^10', 'description^5', 'instructors^2', 'location', 'notes']

    facets = {
        'location': elasticsearch_dsl.TermsFacet(field='location'),
        'instructor': elasticsearch_dsl.TermsFacet(field='instructors'),
        'date': elasticsearch_dsl.DateHistogramFacet(field='date', interval='week'),
        'track': elasticsearch_dsl.TermsFacet(field='track'),
        'open': elasticsearch_dsl.TermsFacet(field='open')
    }

    #def search(self):
    #    ' Override search to add your own filters '
    #    s = super(WorkshopSearch, self).search()
    #    #return s.filter('term', open=True)

