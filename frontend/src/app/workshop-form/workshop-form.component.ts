import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {WorkshopService} from '../workshop.service';
import {Workshop} from "../workshop";
import {Observable} from "rxjs/Observable";

@Component({
  selector: 'app-workshop-form',
  templateUrl: './workshop-form.component.html',
  styleUrls: ['./workshop-form.component.css']
})
export class WorkshopFormComponent implements OnInit {

  workshop_form: FormGroup;
  title: FormControl;
  description: FormControl;
  workshopService: WorkshopService;
  workshop: Observable<Workshop>;

  constructor(workshopService: WorkshopService) {
    this.workshopService = workshopService;
  }

  ngOnInit() {
    this.createFormControls();
    this.createForm();
  }

  createFormControls() {
    this.title = new FormControl('', [Validators.required, Validators.maxLength(256)]);
    this.description = new FormControl('', [Validators.required, Validators.minLength(20)])
  }

  createForm() {
    this.workshop_form = new FormGroup({
      title: this.title,
      description: this.description
    });
  }

  onSubmit() {
    if (this.workshop_form.valid) {
      const workshop = new Workshop();
      workshop.title = this.title.value;
      workshop.description = this.description.value;
      this.workshopService.createWorkshop(workshop)
        .subscribe(
          result => console.log(result),
          error => console.log('ERROR:' + error)
        );
      this.workshop = this.workshopService.createWorkshop(workshop);
    }
  }
}
