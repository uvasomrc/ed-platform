import {Links} from './links';
import {Session} from './session';
import {Review} from './review';
import {Participant} from "./participant";

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = Array<Session>();
  code_id = ''
  instructor: Participant;

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = Array<Session>();
    if ('sessions' in values) {
      for (const s of values['sessions']) {
        this.sessions.push(new Session(s));
      }
    }
    if ('instructor' in values) {
      this.instructor = new Participant(values['instructor']);
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
  wait_listed() { return this.sessions.filter(s => s.wait_listed()).length > 0; }

  hasUpcomingSession(): boolean {
    for (const s of this.sessions) {
      if (s.date_time.valueOf() > Date.now().valueOf()) {
        return true;
      }
    }
    return false;
  }

  replaceSession(session) {
    this.sessions = this.sessions.filter(s => s.id !== session.id);
    this.sessions.push(session);
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


