import {Links} from './links';

export class Participant {

  id: number;
  display_name = '';
  bio = '';
  links = new Links();
  new_account = true;
  use_gravatar = true;
  gravatar = '';

  constructor(values: Object = {}) {
    if (values === null) { return; }
    Object.assign(this, values);
    if ('_links' in values) {
      this.links = new Links(values['_links']);
    }
  }

  image() {
    if (this.use_gravatar) {
      return this.gravatar;
    } else {
      return this.links.image;
    }
  }

}

