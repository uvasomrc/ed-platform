import {Participant} from './participant';
import {Review} from './review';
import {Workshop} from './workshop';
import {Links} from './links';
import {Attendee} from "./attendee";

export class Session {
  id: number;
  date_time: Date;
  duration_minutes: number;
  instructor_notes: string;
  max_attendees: number;
  total_attendees = 0;
  reviews = Array<Review>();
  instructors = Array<Participant>();
  attendees = Array<Participant>();
  workshop: Workshop;
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
                            ps['attended'], ps['created'], this));
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

  getParticipant(id): Participant {
    for (const p of this.attendees) {
      if (p.id === id) {return p;}
    }
  }

  getInstructor(id): Participant {
    for (const p of this.instructors) {
      if (p.id === id) {return p;}
    }
  }


  isPast(): boolean {
    return (this.date_time.valueOf() < new Date().valueOf());
  }

  isAvailable(): boolean {
    return(!this.isPast() && this.max_attendees > this.total_attendees);
  }
}


