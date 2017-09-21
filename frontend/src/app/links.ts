import { environment } from 'environments/environment';

export class Links {
  collection = '';
  image = '';
  self = '';
  workshops = '';
  tracks = '';
  register = '';
  send_email = '';
  messages = '';

  constructor(values: Object = {}) {
    for (const key in values) {
      values[key] = environment.api + values[key];
    }
    Object.assign(this, values);
  }

}
