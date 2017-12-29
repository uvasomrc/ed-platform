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
  max_days_prior: number;
  date_open: Date;
  status: string;
  total_participants = 0;
  reviews = Array<Review>();
  attendees = Array<Participant>();

  links: Links;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    if (values['date_time']) {
      this.date_time = new Date(values['date_time']);
    } else {
      this.date_time = new Date();
    }
    this.links = new Links(values['_links']);
    if ('participant_sessions' in values) {
      for (const ps of values['participant_sessions']) {
        if (ps['review_score']) {
          this.reviews.push(new Review(ps));
        }
        const attendee = new Attendee(ps['participant'],
          ps['attended'], ps['created'], ps['confirmed']);
        this.attendees.push(attendee);
      }
    }
  }

  isFull() {
    return this.max_attendees <= this.total_participants;
  }

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


