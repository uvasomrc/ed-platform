import {Links} from './links';
import {Session} from "./session";
import {ParticipantSession} from "./participant-session";

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = new Array<Session>();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = new Array<Session>();
    if ('sessions' in values) {
      for (let s of values['sessions']) {
        this.sessions.push(new Session(s));
      }
    }
  }

  reviews(): ParticipantSession[] {
    let reviews = new Array<ParticipantSession>();
    for (let s of this.sessions) {
      for (let ps of s.participant_sessions) {
        console.log(JSON.stringify(ps.review_score));
      }
      reviews = reviews.concat(s.participant_sessions.filter(ps =>
        ps.review_score !== null));
    }
    return reviews;
  }

}


