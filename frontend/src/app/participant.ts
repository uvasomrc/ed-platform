import {Links} from './links';
import {Review} from './review';
import {Session} from './session';

export class Participant {

  id: number;
  display_name = '';
  bio = '';
  links = new Links();
  reviews = Array<Review>();
  sessions = Array<Session>();

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    if ('participant_sessions' in values) {
    for (const ps of values['participant_sessions']) {
      if (ps['review_score']) { this.reviews.push(new Review(ps)); }
      if (parent == null) {
        let session = new Session(ps['session'], this);
        session.links.register = ps['_links']['register'];
        this.sessions.push(session);
      }
    }
    }
  }
}

