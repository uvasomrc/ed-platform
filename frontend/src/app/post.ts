import {Participant} from './participant';
export class Post {
  id: number;
  user_id: number;
  posts_count: number;
  created_at: Date;
  display_username = '';
  cooked = '';
  posts: Array<Post>;
  participant: Participant;

  constructor(values: Object = {}) {
    Object.assign(this, values);
    this.posts = Array<Post>();
    if ('posts' in values) {
      for (const p of values['posts']) {
        this.posts.push(new Post(p));
      }
    }
    if ('participant' in values) {
      this.participant = new Participant(values['participant']);
      console.log('The Participant is ' + JSON.stringify(this.participant));
    }
  }
}
