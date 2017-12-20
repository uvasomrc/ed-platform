import { environment } from 'environments/environment';

export class Links {
  collection = '';
  image = '';
  self = '';
  workshops = '';
  workshop = '';
  tracks = '';
  register = '';
  email = '';
  code = '';
  posts = '';
  follow = '';

  constructor(values: Object = {}) {
    for (const key in values) {
      if(!(values[key].substring(0, environment.api.length) === environment.api)) {
        values[key] = environment.api + values[key];
      }
    }
    Object.assign(this, values);
  }

}
