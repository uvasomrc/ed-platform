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
  total_attendees = 0;
  reviews = Array<Review>();
  instructors = Array<Participant>();
  attendees = Array<Participant>();
  links: Links;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.date_time = new Date(values['date_time']);
    this.instructors = new Array<Participant>();
    this.links = new Links(values['_links']);
    if ('participants' in values) {
      for (const ps of values['participants']) {
        if (ps['review_score']) { this.reviews.push(new Review(ps)); }
        this.total_attendees ++;
        this.attendees.push(new Attendee(ps['participant'],
                            ps['attended'], ps['created']));
      }
    }
    if ('instructors' in values) {
      for (const i of values['instructors']) {
        this.instructors.push(new Participant(i));
      }
    }
  }

  unregistered() { return this.status === 'UNREGISTERED'; }
  instructing() { return this.status === 'INSTRUCTOR'; }
  attended() { return this.status === 'ATTENDED'; }
  awaiting_review() { return this.status === 'AWAITING_REVIEW'; }
  registered() { return this.status === 'REGISTERED'; }

  getParticipant(id): Participant {
    for (const p of this.attendees) {
      if (p.id === id) {return p; }
    }
  }

  isInstructor(user: Participant) {
    for (const p of this.instructors) {
      if (p.id === user.id) {return true; }
    }
    return false;
  }

  getInstructor(id): Participant {
    for (const p of this.instructors) {
      if (p.id === id) {return p; }
    }
  }

  firstInstructor(): Participant {
    for (const p of this.instructors) {
      return p;
    }
  }

  isPast(): boolean {
    return (this.date_time.valueOf() < new Date().valueOf());
  }

  isAvailable(): boolean {
    return(!this.isPast() && this.max_attendees > this.total_attendees);
  }

  endTime(): Date {
    const end_date = new Date();
    end_date.setTime(this.date_time.getTime() + (this.duration_minutes * 60 * 1000));
    return end_date;
  }

  instructorsDisplay(): String {
    if (this.instructors.length === 0) {
      return 'Net yet assigned.';
    }
    if (this.instructors.length === 1) {
      return this.instructors[0].display_name;
    } else if (this.instructors.length === 2) {
      return this.instructors[0].display_name +
          ' and ' + this.instructors[1].display_name;
    } else {
      return this.instructors[0].display_name + ' et al.';
    }

  }

}


