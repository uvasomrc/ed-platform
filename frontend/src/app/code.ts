import {Links} from './links';

export class Code {
  id: String;
  prereq: boolean;
  status: String;
  links = new Links();

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.links = new Links(values['_links']);
  }

  attended() { return this.status === 'ATTENDED'; }
  awaiting_review() { return this.status === 'AWAITING_REVIEW'; }
  registered() { return this.status === 'REGISTERED'; }

  color() {
    if (this.attended()) { return 'accent'; }
    if (this.awaiting_review()) { return 'accent'; }
    return 'primary';
  }

  icon() {
    if (this.attended()) { return 'checked'; }
    if (this.awaiting_review()) { return 'checked'; }
    if (this.registered()) { return 'circle-full'; }
    return 'circle-open';
  }

  progress_icon() {
    if (this.prereq) { return 'connector'; }
    return 'connector_blank';
  }


}
