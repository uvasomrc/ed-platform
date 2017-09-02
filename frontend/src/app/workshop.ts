import {Links} from './links';

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
  }

}


