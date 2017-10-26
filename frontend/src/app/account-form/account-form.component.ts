import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from '@angular/router';

@Component({
  selector: 'app-account-form',
  templateUrl: './account-form.component.html',
  styleUrls: ['./account-form.component.scss']
})
export class AccountFormComponent implements OnInit {

  @Input('participant') participant: Participant;
  accountForm: FormGroup;
  displayName: FormControl;
  bio: FormControl;
  imageType: FormControl;
  @ViewChild('fileInput') fileInput: ElementRef;
  selectedImage: String;

  constructor(private accountService: AccountService, private router: Router) {
    this.accountService.getAccount().subscribe(acct => {
      this.participant = acct;
      this.selectedImage = this.participant.image();
    });
  }

  ngOnInit() {
    this.displayName = new FormControl(this.participant.display_name, [Validators.required, Validators.maxLength(256)]);
    this.bio  = new FormControl(this.participant.bio);
    this.imageType = new FormControl(this.participant.use_gravatar ? 'gravatar' : 'uploaded');
    this.accountForm = new FormGroup({
      displayName: this.displayName,
      bio: this.bio,
      imageType: this.imageType
    });
  }

  toggleImage() {
    if (this.imageType.value === 'gravatar') {
      this.participant.use_gravatar = true;
      this.selectedImage = this.participant.gravatar;
    } else {
      this.participant.use_gravatar = false;
      this.selectedImage = this.participant.links.image;
    }
  }

  onSubmit() {
    if (this.accountForm.valid) {
      this.uploadImage();
      const new_account = this.participant.new_account;
      this.participant.display_name = this.displayName.value;
      this.participant.bio = this.bio.value;
      this.participant.new_account = false;
      this.accountService.updatePaticipant(this.participant).subscribe( p => {
        // If this is a new account, then redirect them to page they started on when they hit login, and
        // subsequently got redirected here to complete their details.
        if (new_account) {
          this.router.navigate([this.accountService.getRouteAfterLogin()]);
        }
      });
    }
  }

  uploadImage() {
      const fileIn: HTMLInputElement = this.fileInput.nativeElement;
      if (fileIn.files.length > 0) {
        this.accountService.updateParticipantImage(this.participant, fileIn.files.item(0));
      }
  }

  newImage(event) {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();

      reader.onload = (e2) => {
        this.selectedImage = reader.result;
      };

      reader.readAsDataURL(event.target.files[0]);
    }
  }
}
