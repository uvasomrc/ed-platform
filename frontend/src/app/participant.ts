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
    this.sessions = Array<Session>();
    for (const ps of values['participant_sessions']) {
      if (ps['review_score']) { this.reviews.push(new Review(ps)); }
      if (parent == null) {
        const session = new Session(ps['session'], this);
        this.sessions.push(session);
      }
    }
    }
  }

  upcomingSessions(): Array<Session> {
    return this.sessions.filter( s => {
      return s.date_time.valueOf() >= new Date().valueOf() && s.instructors.filter( i => i.id === this.id).length === 0;
    } );
  }

  pastSessions(): Array<Session> {
    return this.sessions.filter( s => {
      return s.date_time.valueOf() < new Date().valueOf() && s.instructors.filter( i => i.id === this.id).length === 0;
    } );
  }

  teachingSessions(): Array<Session> {
    return this.sessions.filter( s => {
      return s.instructors.filter( i => i.id === this.id).length > 0;
    } );
  }

  isTeacher(): boolean {
    return this.teachingSessions().length > 0;
  }

  isTeaching(session: Session): boolean {
    return (this.teachingSessions().some(s => s.id === session.id));
  }

  isUpcoming(session: Session): boolean {
    return (this.upcomingSessions().some(s => s.id === session.id));
  }

}

