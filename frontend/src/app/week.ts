import {Workshop} from './workshop';

export class Week {
  id: string;
  workshops = Array<Workshop>();
  date: Date;

  constructor(values: Object = {}) {
    Object.assign(this, values);

    if (this.id === '') {
      this.id = 'None scheduled';
    } else {
      this.date = new Date(this.id);
    }


    this.workshops = Array<Workshop>();
    if ('workshops' in values) {
      for (const w of values['workshops']) {
          this.workshops.push(new Workshop(w));
      }
    }
  }

}
