import { Injectable } from '@angular/core';
import {Workshop} from './workshop';
import {ApiService} from './api.service';
import {Observable} from 'rxjs/Observable';
import {Session} from './session';
import {EmailMessage} from './EmailMessage';
import {Search} from './search';
import {Track} from "./track";
import {Post} from "./post";

@Injectable()
export class WorkshopService {

  constructor(private api: ApiService) {}

  // Simulate GET /workshop
  getAllWorkshops(): Observable<Workshop[]> {
    return this.api.getAllWorkshops();
  }

  getWorkshop(id: number): Observable<Workshop> {
    return this.api.getWorkshop(id);
  }

  getSession(id: number): Observable<Session> {
    return this.api.getSession(id);
  }

  getWorkshopForSession(session: Session): Observable<Workshop> {
    return this.api.getWorkshopForSession(session);
  }

  emailParticipants(email: EmailMessage, session: Session): Observable<EmailMessage> {
    return this.api.emailParticipants(email, session);
  }

  getMessages(session: Session): Observable<EmailMessage[]> {
    return this.api.getMessagesForSession(session);
  }

  // Simulate POST /workshop
  addWorkshop(workshop: Workshop): Observable<Workshop> {
    return this.api.addWorkshop(workshop);
  }

  getCodeByString(code: String) {
    return this.api.getCodeByString(code);
  }

  searchWorkshops(search: Search): Observable<Search> {
    return this.api.searchWorkshops(search);
  }

  getTracksForWorkshop(workshop: Workshop): Observable<Track[]> {
    return this.api.getTracksForWorkshop(workshop);
  }

  getPost(workshop: Workshop): Observable<Post> {
    return this.api.getPost(workshop);
  }

}
