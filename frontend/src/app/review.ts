export class Review {
  attended: boolean;
  created: Date;
  is_instructor: boolean;
  review_comment: string;
  review_score: number;
  max_score = 5;

  constructor(values: Object = {}) {
    Object.assign(this, values);
  }


}

