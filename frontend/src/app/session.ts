import {Participant} from './participant';
import {Review} from './review';
import {Workshop} from './workshop';
import {Links} from './links';
import {Attendee} from './attendee';

export class Session {
  id: number;
  date_time: Date;
  duration_minutes: number;
  instructor_notes: string;
  location: string;
  max_attendees: number;
  status: string;
  total_participants: number;
  waiting_participants: number;
  reviews = Array<Review>();
  attendees = Array<Participant>();
  waiting = Array<Participant>();

  links: Links;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.date_time = new Date(values['date_time']);
    this.links = new Links(values['_links']);
    if ('participant_sessions' in values) {
      for (const ps of values['participant_sessions']) {
        if (ps['review_score']) { this.reviews.push(new Review(ps)); }
        const attendee = new Attendee(ps['participant'],
          ps['attended'], ps['created'], ps['wait_listed']);
        if (attendee.wait_listed) {
          this.waiting.push(attendee);
        } else {
          this.attendees.push(attendee);
        }
      }
    }
  }

  isFull() {
    return this.max_attendees <= this.total_participants;
  }

  unregistered() { return this.status === 'UNREGISTERED'; }
  instructing() { return this.status === 'INSTRUCTOR'; }
  attended() { return this.status === 'ATTENDED'; }
  awaiting_review() { return this.status === 'AWAITING_REVIEW'; }
  registered() { return this.status === 'REGISTERED'; }
  wait_listed() {return this.status === 'WAIT_LISTED'; }

  isPast(): boolean {
    return (this.date_time.valueOf() < new Date().valueOf());
  }

  isAvailable(): boolean {
    return(!this.isPast() && this.max_attendees > this.total_participants);
  }

  endTime(): Date {
    const end_date = new Date();
    end_date.setTime(this.date_time.getTime() + (this.duration_minutes * 60 * 1000));
    return end_date;
  }

}


