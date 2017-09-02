import { environment } from 'environments/environment';

export class Links {
  collection = '';
  image = '';
  self = '';
  workshops = '';
  tracks = '';

  constructor(values: Object = {}) {
    for (let key in values) {
      values[key] = environment.api + values[key];
      console.log(key + ' => ' + values[key]);
    }
    Object.assign(this, values);
  }

}
