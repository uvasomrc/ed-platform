import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {WorkshopService} from '../workshop.service';
import {Workshop} from '../workshop';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-workshop-form',
  templateUrl: './workshop-form.component.html',
  styleUrls: ['./workshop-form.component.scss']
})
export class WorkshopFormComponent implements OnInit {

  workshopId = 0;
  workshop: Workshop;
  workshopForm: FormGroup;
  title: FormControl;
  description: FormControl;
  code: FormControl;
  isDataLoaded = false;

  @Output()
  add: EventEmitter<Workshop> = new EventEmitter();

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute,
              private router: Router) {
    this.route.params.subscribe( params =>
      this.workshopId = params['id']);
  }

  ngOnInit() {
    if (this.workshopId > 0){
      this.workshopService.getWorkshop(this.workshopId).subscribe(
        w => {
          this.workshop = w;
          this.loadForm();
       });
    } else {
      this.workshop = new Workshop();
      this.loadForm();
    }
  }

  loadForm() {
    this.title = new FormControl(this.workshop.title, [Validators.required, Validators.maxLength(256)]);
    this.description = new FormControl(this.workshop.description, [Validators.required, Validators.minLength(20)]);

    this.workshopForm = new FormGroup({
      title: this.title,
      description: this.description
    });

    this.title.valueChanges.subscribe(t => this.workshop.title = t);
    this.description.valueChanges.subscribe(d => this.workshop.description = d);

    this.isDataLoaded = true;
  }

  onSubmit() {
    if (this.workshopForm.valid) {
      this.workshopService.addWorkshop(this.workshop).subscribe(newW => {
        this.add.emit(newW);
        this.router.navigate(['workshop', newW.id]);
      });
    }
  }
}
