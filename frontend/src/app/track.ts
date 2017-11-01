import {Links} from './links';
import {Code} from './code';

export class Track {
  title: string;
  description: string;
  image_url: string;
  sub_title: string;
  id: number;
  links = new Links();
  codes = Array<Code>();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.codes = Array<Code>();
    if ('codes' in values) {
      for (const c of values['codes']) {
        this.codes.push(new Code(c));
      }
    }
  }
}
