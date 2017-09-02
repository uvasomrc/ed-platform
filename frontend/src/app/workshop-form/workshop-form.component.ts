import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {WorkshopService} from '../workshop.service';
import {Workshop} from '../workshop';

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

  @Output()
  add: EventEmitter<Workshop> = new EventEmitter();

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
      this.add.emit(workshop);
    }
  }
}
