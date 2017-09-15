import {Links} from './links';
import {Session} from './session';
import {Review} from "./review";

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = new Array<Session>();

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = new Array<Session>();
    if ('sessions' in values && !(parent instanceof Session)) {
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
        if (session == null || s.date_time.valueOf() < session.date.valueOf()) {
          session = s;
        }
      }
    }
    return session;
  }

}


