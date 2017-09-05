import {Links} from './links';
import {Session} from "./session";

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = new Array<Session>();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = new Array<Session>();
    if ('sessions' in values) {
      for (let s of values['sessions']) {
        this.sessions.push(new Session(s));
      }
    }

  }

}


