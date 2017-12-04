import {Component, Inject, OnInit} from '@angular/core';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {TrackService} from '../track.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Code} from '../code';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material';
import {Participant} from '../participant';
import {AccountService} from '../account.service';

@Component({
  selector: 'app-track-details',
  templateUrl: './track-details.component.html',
  styleUrls: ['./track-details.component.scss']
})
export class TrackDetailsComponent implements OnInit {

  track_id = 0;
  track: Track;
  workshops: Workshop[] = [];
  isDataLoaded = false;
  codeIndex = 0;
  code: Code;
  account: Participant;

  constructor(private trackService: TrackService,
              private accountService: AccountService,
              private route: ActivatedRoute,
              private router: Router,
              private dialog: MatDialog) {
    this.route.params.subscribe( params =>
          this.track_id = params['id']);
    this.accountService.getAccount().subscribe( a => this.account = a);
  }

  ngOnInit() {
    this.trackService.getTrack(this.track_id).subscribe(
      (track) => {
        this.track = track;
        this.code = track.codes[this.codeIndex];
        this.isDataLoaded = true;
      }
    );
  }

  prevCode() {
    if (this.codeIndex === 0) {
      return;
    } else {
      this.codeIndex--;
      this.code = this.track.codes[this.codeIndex]
    }
  }

  nextCode() {
    if (this.codeIndex === this.track.codes.length - 1) {
      return;
    } else {
      this.codeIndex++;
      this.code = this.track.codes[this.codeIndex]
    }
  }

  gotoCode(index) {
    this.code = this.track.codes[index];
    this.codeIndex = index;
  }

  confirmDelete() {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      height: '200px',
      width: '300px',
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.trackService.deleteTrack(this.track).subscribe(track => {
            this.router.navigate(['home']);
        });
      }
    });
  }

  editTrack() {
    this.router.navigate(['track-form', this.track.id]);
  }
}

@Component({
  selector: 'app-confirm-dialog',
  templateUrl: 'confirm-dialog.html',
})
export class ConfirmDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
