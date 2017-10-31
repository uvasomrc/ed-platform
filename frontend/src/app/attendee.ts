import {Participant} from './participant';
export class Attendee extends Participant {

  constructor(values: Object = {}, public attended: boolean, public created: Date, public wait_listed: Boolean) {
    super(values);
  }
}
