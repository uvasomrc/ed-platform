import {Session} from './session';

export class EmailMessage {
  id: number;
  subject: String;
  content: String;
  sent_date: Date;
  author_id: number;
  logs: Array<EmailLog>;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
    this.sent_date = new Date(values['sent_date']);
    this.logs = new Array<EmailLog>();
    if ('logs' in values) {
      for (const log of values['logs']) {
        this.logs.push(new EmailLog(log));
      }
    }
  }

  total_delivered() {
    return this.logs.length;
  }

  total_opened() {
    return this.logs.filter(l => l.opened).length;
  }

}

class EmailLog {
  participant_id: number;
  participant_name: string;
  opened: boolean;

  constructor(values: Object = {}, parent = null) {
    Object.assign(this, values);
  }
}
