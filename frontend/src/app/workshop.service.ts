import { Injectable } from '@angular/core';
import {Workshop} from './workshop';
import {ApiService} from './api.service';
import {Observable} from 'rxjs/Observable';
import {Session} from "./session";

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

  // Simulate POST /workshop
  addWorkshop(workshop: Workshop): Observable<Workshop> {
    return this.api.addWorkshop(workshop);
  }
}
