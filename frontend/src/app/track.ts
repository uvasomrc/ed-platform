import {Links} from './links';
export class Track {
  title: string;
  description: string;
  image_url: string;
  id: number;
  links = new Links();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
  }
}
