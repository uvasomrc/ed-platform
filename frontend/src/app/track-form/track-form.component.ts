import {Component, ElementRef, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Track} from '../track';
import {TrackService} from '../track.service';
import {Code} from '../code';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-track-form',
  templateUrl: './track-form.component.html',
  styleUrls: ['./track-form.component.scss']
})
export class TrackFormComponent implements OnInit {

  isDataLoaded = false;
  track: Track;
  trackId: number;
  track_form: FormGroup;
  title: FormControl;
  sub_title: FormControl;
  description: FormControl;
  code: FormControl;
  codeOptions: Code[];
  newTrack: Boolean;
  @ViewChild('fileInput') fileInput: ElementRef;
  imageAdded = false;

  @Output()
  add: EventEmitter<Track> = new EventEmitter();

  constructor(private trackService: TrackService,
              private route: ActivatedRoute,
              private router: Router) {
    this.route.params.subscribe( params =>
      this.trackId = params['id']
    );
  }

  ngOnInit() {
    if (this.trackId > 0) {
      this.trackService.getTrack(this.trackId).subscribe(
        t => {
        this.track = t;
        this.newTrack = false;
        this.loadForm();
        });
    } else {
      this.track = new Track();
      this.newTrack = true;
      this.loadForm();
    }
  }

  loadForm() {
    this.title = new FormControl(this.track.title, [Validators.required, Validators.maxLength(256)]);
    this.description = new FormControl(this.track.description, [Validators.required, Validators.minLength(20)]);
    this.code = new FormControl('');
    this.sub_title = new FormControl(this.track.sub_title);
    this.track_form = new FormGroup({
      title: this.title,
      sub_title: this.sub_title,
      description: this.description,
      code: this.code
    });
    this.trackService.getAllCodes().subscribe(codes => {
      this.codeOptions = codes;
      this.codeOptions = this.codeOptions.filter(c => !this.track.codes.find(tc => tc.id === c.id));
    });

    this.title.valueChanges.subscribe(t => this.track.title = t);
    this.description.valueChanges.subscribe(d => this.track.description = d);
    this.sub_title.valueChanges.subscribe(st => this.track.sub_title = st);

    this.isDataLoaded = true;
  }

  addCodeOption(code) {
    this.codeOptions.push(code);
  }

  setPrereq(index) {
    const code = this.track.codes[index];
    code.prereq = !code.prereq;
  }

  uploadImage() {
    const fileIn: HTMLInputElement = this.fileInput.nativeElement;
    if (fileIn.files.length > 0) {
      this.trackService.updateTrackImage(this.track, fileIn.files.item(0));
    }
  }

  newImage(event) {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (e2) => {
        this.track.links.image = reader.result;
        this.imageAdded = true;
      };

      reader.readAsDataURL(event.target.files[0]);
    }
  }

  onSubmit() {
    console.log("Submitting the form.")
    if (this.track_form.valid) {
      if(this.newTrack) {
        this.trackService.addTrack(this.track).subscribe(newTrack => {
          if (this.imageAdded) { this.uploadImage(); }
          this.add.emit(newTrack);
          this.router.navigate(['track', newTrack.id]);
        });
      } else {
        this.trackService.updateTrack(this.track).subscribe(newTrack => {
          if (this.imageAdded) { this.uploadImage(); }
          this.add.emit(newTrack);
          this.router.navigate(['track', newTrack.id]);
        });
      }
    }
  }
}
