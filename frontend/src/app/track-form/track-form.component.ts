import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Track} from '../track';
import {TrackService} from '../track.service';
import {Code} from '../code';
import {Router} from "@angular/router";

@Component({
  selector: 'app-track-form',
  templateUrl: './track-form.component.html',
  styleUrls: ['./track-form.component.scss']
})
export class TrackFormComponent implements OnInit {

  track: Track;
  track_form: FormGroup;
  title: FormControl;
  sub_title: FormControl;
  description: FormControl;
  code: FormControl;
  codeOptions: Code[];

  @Output()
  add: EventEmitter<Track> = new EventEmitter();

  constructor(private trackService: TrackService,
              private router: Router) {}

  ngOnInit() {
    this.track = new Track();

    this.title = new FormControl('', [Validators.required, Validators.maxLength(256)]);
    this.description = new FormControl('', [Validators.required, Validators.minLength(20)]);
    this.code = new FormControl('', [Validators.required]);
    this.sub_title = new FormControl('');
    this.track_form = new FormGroup({
      title: this.title,
      sub_title: this.sub_title,
      description: this.description,
      code: this.code
    });
    this.trackService.getAllCodes().subscribe(codes => this.codeOptions = codes);

    this.title.valueChanges.subscribe(t => this.track.title = t);
    this.description.valueChanges.subscribe(d => this.track.description = d);
    this.sub_title.valueChanges.subscribe(st => this.track.sub_title = st);
  }

  addCode() {
    const code = this.codeOptions.filter(c => c.id === this.code.value)[0];
    console.log("Adding Code: " + code);
    this.track.codes.push(code);
  }

  setPrereq(index) {
    const code = this.track.codes[index];
    code.prereq = !code.prereq;
  }

  onSubmit() {
    if (this.track_form.valid) {
      this.track.title = this.title.value;
      this.track.description = this.description.value;
      console.log("The codes are " + this.track.codes);
      this.trackService.addTrack(this.track).subscribe(newTrack => {
        this.track = newTrack;
        this.add.emit(this.track);
        this.router.navigate(['home']);
      });
    }
  }
}
