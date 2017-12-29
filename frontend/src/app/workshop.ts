import {Links} from './links';
import {Session} from './session';
import {Review} from './review';
import {Participant} from './participant';

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = Array<Session>();
  code_id = '';
  instructor: Participant;
  followers: Participant[];
  discourse_enabled = false;
  discourse_url = '';
  discourse_topic_id: Number;
  status = '';

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
    if ('followers' in values) {
      this.followers = Array<Participant>();
      for (const f of values['followers']) {
        this.followers.push(new Participant(f));
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


