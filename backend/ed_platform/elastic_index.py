from flask import logging

from elasticsearch_dsl import DocType, Date, Float, Keyword, Text, \
    Index, Search, analyzer, Nested, Integer, analysis, Q, tokenizer
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
        self.index_prefix = app.config['ELASTIC_SEARCH']["index_prefix"]

        self.workshop_index_name = '%s_workshops' % self.index_prefix
        self.workshop_index = Index(self.workshop_index_name)
        self.workshop_index.doc_type(ElasticWorkshop)

        self.participant_index_name = '%s_participants' % self.index_prefix
        self.participant_index = Index(self.participant_index_name)
        self.participant_index.doc_type(ElasticParticipant)

        try:
            ElasticWorkshop.init()
            ElasticParticipant.init()
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
            self.workshop_index.delete(ignore=404)
            self.participant_index.delete(ignore=404)
            ElasticWorkshop.init()
            ElasticParticipant.init()
        except:
            self.logger.error("Failed to delete the indices.  They night not exist.")

    def load_workshops(self, workshops):
        print ("Loading workshops into %s" % self.index_prefix)
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

            if(ew.instructor != None) :
                ew.instructor.append(w.instructor.display_name)
                ew.instructor_search.append(w.instructor.display_name)

            for s in w.sessions:
                ew.date.append(s.date_time)
                ew.location.append(s.location)
                ew.location_search.append(s.location)
                ew.open.append(s.is_open()),
                ew.full.append(s.is_full()),
                ew.notes.append(s.instructor_notes)
                for email in s.email_messages:
                    ew.messages.append(email.content)
                    ew.messages.append(email.subject)
            ElasticWorkshop.save(ew)
        self.workshop_index.flush()

    def load_participants(self, participants):
        print("Loading participants into the Elastic Index... ")
        for p in participants:
            ep = ElasticParticipant(meta={'id': 'participant_' + str(p.id)},
                                    id=p.id,
                                    uid=p.uid,
                                    title=p.title,
                                    display_name=p.display_name,
                                    bio=p.bio,
                                    created=p.created
                                   )
            ElasticParticipant.save(ep)
            self.participant_index.flush()

    def search_workshops(self, search):
        workshop_search = WorkshopSearch(search.query, search.jsonFilters(),
                                         date_restriction=search.date_restriction, index=self.workshop_index_name)
        # apply pagination arguments...
        workshop_search = workshop_search[search.start:search.start + search.size]
        return workshop_search.execute()

    def search_participants(self, search):
        fields = ['uid^10', 'display_name^5', 'bio']
        if search.query == "":
            q = Q("match_all")
        else:
            q = Q("multi_match", query=search.query, fields=fields)
        s = Search(index=self.participant_index_name).query(q)
        return s.execute()

autocomplete = analyzer('autocomplete',
    tokenizer=tokenizer('ngram', 'edge_ngram', min_gram=2, max_gram=15, token_chars=["letter","digit"]),
    filter=['lowercase']
)
autocomplete_search = analyzer('autocomplete_search',
    tokenizer=tokenizer('lowercase')
)

class ElasticParticipant(DocType):
    id = Integer()
    title = Text()
    uid = Keyword()
    display_name = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    bio = Text()
    created = Date()


class ElasticWorkshop(DocType):
    """A flattened version of the index where Title, SelfText, and Comment Text are all top level documents"""
    id = Integer()
    title = Text(analyzer=autocomplete, search_analyzer=autocomplete_search)
    description = Text()
    code = Text()
    date = Date(multi=True)
    location = Keyword(multi=True)
    location_search = Text(multi=True)
    open = Keyword(multi=True)
    full = Keyword(multi=True)
    notes = Text(multi=True)
    messages = Text(multi=True)
    instructor = Keyword(multi=True)
    instructor_search = Text(multi=True)
    tracks = Keyword(multi=True)

class WorkshopSearch(elasticsearch_dsl.FacetedSearch):

    def __init__(self, *args, **kwargs):
        self.index = kwargs["index"]
        self.date_restriction = kwargs["date_restriction"]
        kwargs.pop("index")
        kwargs.pop("date_restriction")
        super(WorkshopSearch, self).__init__(*args, **kwargs)

    doc_types = [ElasticWorkshop]
    fields = ['title^10', 'description^5', 'instructor_search^2', 'location_search', 'notes']

    facets = {
        'location': elasticsearch_dsl.TermsFacet(field='location'),
        'instructor': elasticsearch_dsl.TermsFacet(field='instructor'),
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

