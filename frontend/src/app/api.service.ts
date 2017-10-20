import { Injectable } from '@angular/core';
import { environment } from 'environments/environment';
import {Http, RequestOptions, Headers, Response} from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import {Workshop} from './workshop';
import {Track} from './track';
import {Participant} from './participant';
import {Session} from './session';
import {EmailMessage} from './EmailMessage';
import {Search} from './search';
import {Code} from './code';

@Injectable()
export class ApiService {

  apiRoot = environment.api;
  workshop_url = `${this.apiRoot}/api/workshop`;
  search_url = `${this.apiRoot}/api/workshop/search`;
  track_url = `${this.apiRoot}/api/track`;
  session_url = `${this.apiRoot}/api/session`;
  account_url = `${this.apiRoot}/api/user`;

  token: string;

  constructor(private http: Http) {
    if (localStorage.getItem('token') !== null &&
        localStorage.getItem('token') !== 'undefined') {
      this.token = JSON.parse(localStorage.getItem('token'));
    }
  }

  getOptions(): RequestOptions {
    const headers = new Headers({'Authorization': 'Bearer ' + this.token});
    const options = new RequestOptions({headers: headers});
    return options;
  }

  login(token): Observable<Participant> {
    this.token = token;
    localStorage.setItem('token', JSON.stringify(token));
    console.log('The Token Is Set To:' + this.token);
    return this.http.get(this.account_url, this.getOptions())
      .map(res => { return new Participant(res.json()); })
      .catch(this.handleError);
  }

  getAccount(): Observable<Participant> {
    return this.http.get(this.account_url, this.getOptions())
      .map(res => { return new Participant(res.json()); })
      .catch(this.handleError);
  }

  logout() {
    this.token = '';
    localStorage.removeItem('token');
  }

  unRegister(session: Session): Observable<Session> {
    return this.http.delete(session.links.register, this.getOptions())
      .map(res => { return new Session(res.json()); })
      .catch(this.handleError);
  }

  register(session: Session): Observable<Session> {
    return this.http.post(session.links.register, '{}', this.getOptions())
      .map(res => { return new Session(res.json()); })
      .catch(this.handleError);
  }

  emailParticipants(email: EmailMessage, session: Session): Observable<EmailMessage> {
    return this.http.post(session.links.send_email, email, this.getOptions())
      .map(res => {
        return new EmailMessage(res.json());
      })
      .catch(this.handleError);
  }

  getMessagesForSession(session: Session): Observable<EmailMessage[]> {
    return this.http.get(session.links.messages, this.getOptions())
      .map(res => {
        return res.json().map(item => {
          return (new EmailMessage(item));
        });
      })
      .catch(this.handleError);
  }


  getTracks(): Observable<Track[]> {
    return this.http.get(this.track_url, this.getOptions())
      .map(res => {
        return res.json().tracks.map(item => {
          return(new Track(item));
        });
      });
  }

  getTrack(track_id: number): Observable<Track> {
    return this.http.get(this.track_url + '/' + track_id, this.getOptions())
      .map(res => {
        return new Track(res.json());
        });
  }

  getCode(code: Code): Observable<Code> {
    return this.http.get(code.links.self, this.getOptions())
      .map(res => {
          return(new Code(res.json()));
      });
  }

  getAllWorkshops(): Observable<Workshop[]> {
    return this.http.get(this.workshop_url, this.getOptions())
      .map(res => {
        return res.json().workshops.map(item => {
          return(new Workshop(item));
        });
      });
  }

  searchWorkshops(search: Search): Observable<Search> {
    return this.http
      .post(this.search_url, search, this.getOptions())
      .map(response => {
        return new Search(response.json());
      })
      .catch(this.handleError);
  }

  getWorkshop(workshop_id: number): Observable<Workshop> {
    return this.http.get(this.workshop_url + '/' + workshop_id, this.getOptions())
      .map(res => {
        return new Workshop(res.json());
      });
  }

  getCodeForWorkshop(workshop: Workshop): Observable<Code> {
    return this.http.get(workshop.links.code, this.getOptions())
      .map(res => {
        return(new Code(res.json()));
      });
  }

  getTracksForWorkshop(workshop: Workshop): Observable<Track[]> {
    return this.http.get(workshop.links.tracks, this.getOptions())
      .map(res => {
        return res.json().map(item => {
          return(new Track(item));
        });
      });
  }

  getWorkshopForSession(session: Session): Observable<Workshop> {
    return this.http.get(session.links.workshop, this.getOptions())
      .map(res => {
        return new Workshop(res.json());
      });
  }

  getWorkshopsForParticipant(participant: Participant): Observable<Workshop[]> {
    return this.http.get(participant.links.workshops, this.getOptions())
      .map(res => {
        return res.json().map(item => {
          return(new Workshop(item));
        });
      });
  }


  getSession(session_id: number): Observable<Session> {
    return this.http.get(this.session_url + '/' + session_id, this.getOptions())
      .map(res => {
        return new Session(res.json());
      });
  }

  public addWorkshop(workshop: Workshop): Observable<Workshop> {
    return this.http
      .post(this.workshop_url, workshop, this.getOptions())
      .map(response => {
        return new Workshop(response.json());
      })
      .catch(this.handleError);
  }

  private handleError (error: Response | any) {
    console.error('ApiService::handleError', error);
    return Observable.throw(error);
  }





  /*

  public getAllTodos(): Observable<Todo[]> {
    return this.http
      .get(API_URL + '/todos')
      .map(response => {
        const todos = response.json();
        return todos.map((todo) => new Todo(todo));
      })
      .catch(this.handleError);
  }


  public getTodoById(todoId: number): Observable<Todo> {
    return this.http
      .get(API_URL + '/todos/' + todoId)
      .map(response => {
        return new Todo(response.json());
      })
      .catch(this.handleError);
  }

  public updateTodo(todo: Todo): Observable<Todo> {
    return this.http
      .put(API_URL + '/todos/' + todo.id, todo)
      .map(response => {
        return new Todo(response.json());
      })
      .catch(this.handleError);
  }

  public deleteTodoById(todoId: number): Observable<null> {
    return this.http
      .delete(API_URL + '/todos/' + todoId)
      .map(response => null)
      .catch(this.handleError);
  }

*/

}
