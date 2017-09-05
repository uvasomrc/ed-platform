import {Participant} from './participant';
import {Links} from './links';
import {ParticipantSession} from './participant-session';

export class Session {
  id: number;
  date_time: Date;
  duration_minutes: number;
  instructor_notes: string;
  participant_sessions: ParticipantSession[];

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.date_time = new Date(values['date_time']);
    this.participant_sessions = new Array<ParticipantSession>();
    if ('participant_sessions' in values) {
      for (let ps of values['participant_sessions']) {
        this.participant_sessions.push(new ParticipantSession(ps));
      }
    }
    /*
    for (let ps of values['participant_sessions']) {
      this.participant_sessions.push(new ParticipantSession(ps));
    }
    */
  }
}


