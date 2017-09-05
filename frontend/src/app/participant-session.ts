import {Participant} from './participant';

export class ParticipantSession {
  attended: boolean;
  created: Date;
  is_instructor: boolean;
  review_comment: string;
  reivew_score: number;
  participant: Participant;

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.participant = new Participant(values['participant']);
  }

}

