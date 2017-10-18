import {Links} from './links';

export class Participant {

  id: number;
  display_name = '';
  bio = '';
  links = new Links();

  constructor(values: Object = {}) {
    if (values === null) { return; }
    Object.assign(this, values);
    if ('_links' in values) {
      this.links = new Links(values['_links']);
    }
  }

}

