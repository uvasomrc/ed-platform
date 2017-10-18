import {Links} from './links';
import {Session} from './session';
import {Review} from './review';

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = Array<Session>();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = Array<Session>();
    if ('sessions' in values) {
      for (const s of values['sessions']) {
        this.sessions.push(new Session(s));
      }
    }
  }

  reviews(): Review[] {
    let reviews = new Array<Review>();
    for (const s of this.sessions) {
      reviews = reviews.concat(s.reviews);
    }
    return reviews;
  }

  instructing() { return this.sessions.filter(s => s.instructing()).length > 0; }
  attended() { return this.sessions.filter(s => s.attended()).length > 0; }
  awaiting_review() { return this.sessions.filter(s => s.awaiting_review()).length > 0; }
  registered() { return this.sessions.filter(s => s.registered()).length > 0; }

  hasUpcomingSession(): boolean {
    for (const s of this.sessions) {
      if (s.date_time.valueOf() > Date.now().valueOf()) {
        return true;
      }
    }
    return false;
  }

  nextSession(): Session {
    let session = null;
    for (const s of this.sessions) {
      if (s.date_time.valueOf() > Date.now().valueOf()) {
        if (session == null || s.date_time.valueOf() < session.date_time.valueOf()) {
          session = s;
        }
      }
    }
    return session;
  }

}


