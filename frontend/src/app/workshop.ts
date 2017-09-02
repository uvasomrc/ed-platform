export class Workshop {

  id: number;
  title = '';
  description = '';

  constructor(values: Object = {}) {
    Object.assign(this, values);
  }
}


