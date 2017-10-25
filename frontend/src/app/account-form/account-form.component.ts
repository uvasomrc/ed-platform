import {Component, Input, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from '@angular/router';

@Component({
  selector: 'app-account-form',
  templateUrl: './account-form.component.html',
  styleUrls: ['./account-form.component.css']
})
export class AccountFormComponent implements OnInit {

  @Input('participant') participant: Participant;
  accountForm: FormGroup;
  displayName: FormControl;
  bio: FormControl;
  image: FormControl;

  constructor(private accountService: AccountService, private router: Router) {
    this.accountService.getAccount().subscribe(acct => {
      this.participant = acct;
    });
  }

  ngOnInit() {
    this.displayName = new FormControl(this.participant.display_name, [Validators.required, Validators.maxLength(256)]);
    this.bio  = new FormControl(this.participant.bio, []);
    this.accountForm = new FormGroup({
      displayName: this.displayName,
      bio: this.bio
    });
  }

  onSubmit() {
    if (this.accountForm.valid) {
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


}
