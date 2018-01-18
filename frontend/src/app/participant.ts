import {Links} from './links';

export class Participant {

  id: number;
  uid = '';
  display_name = '';
  bio = '';
  title = '';
  email_address = '';
  phone_number = '';
  role = '';
  links = new Links();
  new_account = true;
  use_gravatar = true;
  gravatar = '';
  created: Date;



  constructor(values: Object = {}) {
    if (values === null) { return; }
    Object.assign(this, values);
    if ('_links' in values) {
      this.links = new Links(values['_links']);
    }
  }

  isAdmin() {
    return this.role === 'ADMIN';
  }

  image() {
    if (this.use_gravatar) {
      return this.gravatar;
    } else {
      return this.links.image;
    }
  }

}

