import {Component, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {WorkshopService} from '../workshop.service';
import {Workshop} from '../workshop';
import {ActivatedRoute, Router} from '@angular/router';
import {Participant} from '../participant';
import {Session} from '../session';
import {SessionFormComponent} from '../session-form/session-form.component';
import {Code} from '../code';
import {TrackService} from '../track.service';

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
  discourse_enabled: FormControl;
  discourse_topic_id: FormControl;
  code: FormControl;
  isDataLoaded = false;
  codeList = new Array<Code>();

  @Output()
  add: EventEmitter<Workshop> = new EventEmitter();

  @ViewChild(SessionFormComponent) sessionForm: SessionFormComponent;

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService,
              private route: ActivatedRoute,
              private router: Router) {
    this.route.params.subscribe( params =>
      this.workshopId = params['id']);
  }

  ngOnInit() {
    this.loadWorkshop();
    this.loadCodes();
  }

  loadCodes() {
    this.trackService.getAllCodes().subscribe( codes => this.codeList = codes);
  }

  loadWorkshop() {
    if (this.workshopId > 0) {
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

  setInstructor(p: Participant) {
    console.log(`Setting instructor to ${p.display_name}`);
    this.workshop.instructor = p;
  }

  loadForm() {
    this.title = new FormControl([Validators.required, Validators.maxLength(256)]);
    this.description = new FormControl([Validators.required, Validators.minLength(20)]);
    this.discourse_enabled = new FormControl();
    this.code = new FormControl();
    this.discourse_topic_id = new FormControl();

    this.workshopForm = new FormGroup({
      title: this.title,
      description: this.description,
      discourse_enabled: this.discourse_enabled,
      discourse_topic_id: this.discourse_topic_id,
      code: this.code
    });

    this.code.patchValue(this.workshop.code_id);
    this.title.patchValue(this.workshop.title);
    this.description.patchValue(this.workshop.description);
    this.discourse_enabled.patchValue(this.workshop.discourse_enabled);
    this.discourse_topic_id.patchValue(this.workshop.discourse_topic_id);

    this.title.valueChanges.subscribe(t => this.workshop.title = t);
    this.description.valueChanges.subscribe(d => this.workshop.description = d);
    this.code.valueChanges.subscribe(code_id => this.workshop.code_id = code_id);
    this.discourse_enabled.valueChanges.subscribe(enabled => this.workshop.discourse_enabled = enabled);
    this.discourse_topic_id.valueChanges.subscribe(id => this.workshop.discourse_topic_id = id);
    this.isDataLoaded = true;
  }

  addSession(s: Session) {
    console.log(`Adding Session ${s.id}`);
    const index = this.workshop.sessions.findIndex(es => es.id === s.id);
    if (!s.id) {
      s.id = 0 - this.workshop.sessions.length;
    }
    if (index >= 0) {
      this.workshop.sessions[index] = s;
    } else {
      this.workshop.sessions.push(s);
    }
  }

  deleteSession(s: Session) {
    console.log(`Removing Session ${s.id}`);
    const index = this.workshop.sessions.findIndex(es => es.id === s.id);
    if (index >= 0) {
      this.workshop.sessions.splice(index, 1);
    }
  }

  editSession(s: Session) {
    // If the id is 0, give it a negative number, so we know what it is
    // when it comes back.
    this.sessionForm.editSession(s);
  }

  onSubmit() {
    if (this.workshopForm.valid) {
      this.workshopService.addWorkshop(this.workshop).subscribe(newW => {
        this.add.emit(newW);
        this.router.navigate(['workshop', newW.id]);
      });
    }
  }

  onReset() {
    this.loadWorkshop();
  }

}
