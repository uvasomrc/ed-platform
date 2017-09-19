import { Component, OnInit } from '@angular/core';
import {Participant} from '../participant';
import {Session} from '../session';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-teacher-dashboard',
  templateUrl: './teacher-dashboard.component.html',
  styleUrls: ['./teacher-dashboard.component.css']
})
export class TeacherDashboardComponent implements OnInit {

  account: Participant;
  session: Session;
  session_id = 0;
  is_data_loaded = false;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.session_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getSession(this.session_id).subscribe(
      session => {
        this.session = session;
        this.is_data_loaded = true;
      }
    );
  }

}
