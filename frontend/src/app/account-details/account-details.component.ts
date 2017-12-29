import {AfterViewInit, ChangeDetectorRef, Component, Inject, OnInit} from '@angular/core';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Workshop} from '../workshop';
import {MAT_DIALOG_DATA, MatDialog} from "@angular/material";

@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.scss']
})
export class AccountDetailsComponent implements OnInit, AfterViewInit {

  participant: Participant;
  workshops: Workshop[];
  isDataLoaded = false;

  constructor(private accountService: AccountService, private dialog: MatDialog,
              private _changeDetectionRef: ChangeDetectorRef) {}

  ngOnInit() {
    this.accountService.getAccount().subscribe(acct => {
      this.participant = acct;
      if (this.participant.new_account) {
        this.openDialog();
        this._changeDetectionRef.detectChanges();
      }
      this.accountService.getWorkshopsForParticipant(acct).subscribe(ws => {
        this.workshops = ws;
        this.isDataLoaded = true;
      });
    });
  }

  ngAfterViewInit() {
  }

  openDialog() {
    this.dialog.open(NewUserDialogComponent, {
      width: '250px'
    });
  }

  upcomingWorkshops() {
    return this.workshops.filter(ws => ws.status === 'REGISTERED');
  }

  pastWorkshops() {
    return this.workshops.filter(ws => ws.status === 'ATTENDED');
  }

  instructingWorkshops() {
    return this.workshops.filter(ws => ws.status === 'INSTRUCTOR');
  }


}

@Component({
  selector: 'app-new-user-dialog',
  templateUrl: 'new-user-dialog.html',
})
export class NewUserDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
