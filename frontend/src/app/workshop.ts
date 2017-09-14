import {Links} from './links';
import {Session} from './session';
import {Review} from "./review";

export class Workshop  {

  id: number;
  title = '';
  description = '';
  links = new Links();
  sessions = new Array<Session>();

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
    this.sessions = new Array<Session>();
    if ('sessions' in values && !(parent instanceof Session)) {
      for (const s of values['sessions']) {
        this.sessions.push(new Session(s));
      }
    }
  }

  reviews(): Review[] {
    let reviews = new Array<Review>();
    for (const s of this.sessions) {
      reviews = reviews.concat(s.reviews);
    }
    return reviews;
  }

}


