import {Links} from "./links";

export class Participant {

  id: number;
  display_name = '';
  bio = '';
  links = new Links();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
  }
}
