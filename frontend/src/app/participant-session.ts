import {Participant} from './participant';

export class ParticipantSession {
  attended: boolean;
  created: Date;
  is_instructor: boolean;
  review_comment: string;
  review_score: number;
  participant: Participant;
  max_score = 5;

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.participant = new Participant(values['participant']);
  }

}

