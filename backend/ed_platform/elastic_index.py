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
        if(settings["http_auth_user"] != ''):
            self.connection = connections.create_connection(hosts=settings["hosts"],
                                                        port=settings["port"],
                                                        timeout=settings["timeout"],
                                                        verify_certs=settings["verify_certs"],
                                                        use_ssl=settings["use_ssl"],
                                                        http_auth=(settings["http_auth_user"],
                                                                   settings["http_auth_pass"]))
        else:
            # Don't set an http_auth at all for connecting to AWS ElasticSearch or you will
            # get a cryptic message that is darn near ungoogleable.
            self.connection = connections.create_connection(hosts=settings["hosts"],
                                                            port=settings["port"],
                                                            timeout=settings["timeout"],
                                                            verify_certs=settings["verify_certs"],
                                                            use_ssl=settings["use_ssl"])
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
                                 description=w.description
                                 )
            if(w.code != None):
                ew.code = w.code.id

                for tc in w.code.track_codes:
                    print("The Track Id is " + str(tc.track_id))
                    ew.tracks.append(tc.track.title)

            for s in w.sessions:
                ew.date.append(s.date_time)
                ew.location.append(s.location)
                ew.location_search.append(s.location)
                ew.open.append(s.open()),
                ew.notes.append(s.instructor_notes)
                for email in s.email_messages:
                    ew.messages.append(email.content)
                    ew.messages.append(email.subject)
                for instructor in s.instructors():
                    ew.instructors.append(instructor.display_name)
                    ew.instructors_search.append(instructor.display_name)
            ElasticWorkshop.save(ew)
        self.index.flush()

    def search(self, search):
        # when using:
        #        workshop_search = BlogSearch("web framework", filters={"category": "python"})
        workshop_search = WorkshopSearch(search.query, search.jsonFilters(),
                                         date_restriction=search.date_restriction, index=self.index_name)
        #workshop_search = WorkshopSearch(search.query, index=self.index_name)
        return workshop_search.execute()


class ElasticWorkshop(DocType):
    """A flattened version of the index where Title, SelfText, and Comment Text are all top level documents"""
    id = Integer()
    title = Text()
    description = Text()
    code = Text()
    date = Date(multi=True)
    location = Keyword(multi=True)
    location_search = Text(multi=True)
    open = Keyword(multi=True)
    notes = Text(multi=True)
    messages = Text(multi=True)
    instructors = Keyword(multi=True)
    instructors_search = Text(multi=True)
    tracks = Keyword(multi=True)

class WorkshopSearch(elasticsearch_dsl.FacetedSearch):

    def __init__(self, *args, **kwargs):
        self.index = kwargs["index"]
        self.date_restriction = kwargs["date_restriction"]
        kwargs.pop("index")
        kwargs.pop("date_restriction")
        super(WorkshopSearch, self).__init__(*args, **kwargs)

    doc_types = [ElasticWorkshop]
    fields = ['title^10', 'description^5', 'instructors_search^2', 'location_search', 'notes']

    facets = {
        'location': elasticsearch_dsl.TermsFacet(field='location'),
        'instructors': elasticsearch_dsl.TermsFacet(field='instructors'),
        'tracks': elasticsearch_dsl.TermsFacet(field='tracks')
#        'date': elasticsearch_dsl.DateHistogramFacet(field='date', interval='week'),
#        'open': elasticsearch_dsl.TermsFacet(field='open')
    }

    def search(self):
        ' Override search to add your own filters '
        s = super(WorkshopSearch, self).search()
        if(self.date_restriction.lower() == "past"):
            s = s.filter('range',date={"lte": "now-1d/d"})
        if (self.date_restriction.lower() == "future"):
            s = s.filter('range',date={"gt": "now-1d/d"})
        if (self.date_restriction.lower() == "7days"):
            s = s.filter('range',date={"gt": "now-1d/d","lte":"now+7d/d"})
        if (self.date_restriction.lower() == "30days"):
            s = s.filter('range',date={"gt": "now-1d/d", "lte": "now+30d/d"})
        return s

