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

@Injectable()
export class ApiService {

  apiRoot = environment.api;
  workshop_url = `${this.apiRoot}/api/workshop`;
  track_url = `${this.apiRoot}/api/track`;
  account_url = `${this.apiRoot}/api/auth`;
  token: string;

  constructor(private http: Http) {
    this.token = JSON.parse(localStorage.getItem('token'));
    console.log('The Token At Construction is:' + this.token);
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', JSON.stringify(token));
    console.log('The Token Is Set To:' + this.token);
  }

  logout() {
    this.token = '';
    localStorage.removeItem('token');
  }

  getOptions(): RequestOptions {
    let headers = new Headers({'Authorization': 'Bearer ' + this.token});
    let options = new RequestOptions({headers: headers});
    return options;
  }

  getTracks(): Observable<Track[]> {
    return this.http.get(this.track_url)
      .map(res => {
        return res.json().tracks.map(item => {
          return(new Track(item));
        });
      });
  }

  getTrack(track_id: number): Observable<Track> {
    return this.http.get(this.track_url + '/' + track_id)
      .map(res => {
        return new Track(res.json());
        });
  }

  getAccount(): Observable<Participant> {
    return this.http.get(this.account_url, this.getOptions())
      .map(res => {
        return new Participant(res.json());
      });
  }


  getTrackWorkshops(track: Track): Observable<Workshop[]> {
    console.log('Calling: ' + track.links.workshops);
    return this.http.get(track.links.workshops)
      .map(res => {
        return res.json().workshops.map(item => {
          return(new Workshop(item));
        });
      });
  }

  getAllWorkshops(): Observable<Workshop[]> {
    return this.http.get(this.workshop_url)
      .map(res => {
        return res.json().workshops.map(item => {
          return(new Workshop(item));
        });
      });
  }

  getWorkshop(workshop_id: number): Observable<Workshop> {
    return this.http.get(this.workshop_url + '/' + workshop_id)
      .map(res => {
        return new Workshop(res.json());
      });
  }

  public addWorkshop(workshop: Workshop): Observable<Workshop> {
    return this.http
      .post(this.workshop_url, workshop)
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
