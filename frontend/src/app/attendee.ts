import {Participant} from "./participant";
export class Attendee extends Participant {

  constructor(values: Object = {}, private attended: boolean, private created: Date, parent = null) {
    super(values, parent);
  }
}
