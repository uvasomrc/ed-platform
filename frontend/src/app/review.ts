import {Participant} from "./participant";
export class Review {
  attended: boolean;
  created: Date;
  is_instructor: boolean;
  review_comment: string;
  review_score: number;
  max_score = 5;
  participant: Participant;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);

    if ('participant' in values && !(parent instanceof Participant)) {
      this.participant = new Participant(values['participant']);
    }
  }


}

