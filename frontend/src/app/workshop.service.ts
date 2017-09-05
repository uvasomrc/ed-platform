import { Injectable } from '@angular/core';
import {Workshop} from './workshop';
import {ApiService} from './api.service';
import {Observable} from 'rxjs/Observable';

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

  // Simulate POST /workshop
  addWorkshop(workshop: Workshop): Observable<Workshop> {
    return this.api.addWorkshop(workshop);
  }
}
