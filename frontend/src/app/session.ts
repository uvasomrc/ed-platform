import {Participant} from './participant';
import {Review} from './review';
import {Workshop} from './workshop';
import {Links} from './links';

export class Session {
  id: number;
  date_time: Date;
  duration_minutes: number;
  instructor_notes: string;
  max_attendees: number;
  total_attendees = 0;
  reviews = Array<Review>();
  instructors = Array<Participant>();
  workshop: Workshop;
  links: Links;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.date_time = new Date(values['date_time']);
    this.instructors = new Array<Participant>();
    this.links = new Links(values['_links']);
    if ('participant_sessions' in values) {
      this.total_attendees ++;
      for (const ps of values['participant_sessions']) {
        if (ps['review_score']) { this.reviews.push(new Review(ps)); }
      }
    }
    if ('instructors' in values) {
      for (const i of values['instructors']) {
        this.instructors.push(new Participant(i, this));
      }
    }
    if ('workshop' in values && !(parent instanceof Workshop)) {
      this.workshop = new Workshop(values['workshop']);
    }
  }

  isPast(): boolean {
    return (this.date_time.valueOf() < new Date().valueOf());
  }

  isAvailable(): boolean {
    return(!this.isPast() && this.max_attendees > this.total_attendees);
  }
}


