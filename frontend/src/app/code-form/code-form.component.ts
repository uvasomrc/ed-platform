import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {Code} from '../code';
import {TrackService} from '../track.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-code-form',
  templateUrl: './code-form.component.html',
  styleUrls: ['./code-form.component.scss']
})
export class CodeFormComponent implements OnInit {

  code: Code;
  codeForm: FormGroup;
  name: FormControl;
  description: FormControl;

  @Output()
  add: EventEmitter<Code> = new EventEmitter();

  constructor(private trackService: TrackService) { }

  ngOnInit() {
    this.code = new Code();
    this.name = new FormControl('', [Validators.required, Validators.maxLength(50)]);
    this.description = new FormControl('', [Validators.required, Validators.minLength(20)]);

    this.codeForm = new FormGroup({
      name: this.name,
      description: this.description
    });
    this.name.valueChanges.subscribe(n => this.code.id = n);
    this.description.valueChanges.subscribe(n => this.code.description = n);
  }

  onSubmit() {
    if (this.codeForm.valid) {
      this.trackService.addCode(this.code).subscribe(newCode => {
        this.add.emit(newCode);
        this.codeForm.reset();
        this.code = new Code;
      });
    }
  }


}
