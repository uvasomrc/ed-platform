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
  isDataLoaded = false;
  codeIndex = 0;
  code: Code;
  account: Participant;
  weeks = [];
  workshop_groups = [];
  view_type = 'code';

  private swipeCoord?: [number, number];
  private swipeTime?: number;

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
        this.workshop_groups = track.codes;

        for (let i = 0; i < track.codes.length; i++) {
          this.trackService.getCode(track.codes[i]).subscribe(
            (c) => {
                track.codes[i].workshops = c.workshops;
            });
        }

        this.trackService.getTrackWorkshopsByDate(this.track).subscribe(
          (weeks) => {
            this.weeks = weeks;
        });
      }
    );
  }

  toggle_list() {
    if(this.view_type === 'code') {
      this.workshop_groups = this.weeks;
      this.view_type = 'week';
    } else {
      this.view_type = 'code';
      this.workshop_groups = this.track.codes;
    }
    this.codeIndex = 0;
    this.code = this.workshop_groups[this.codeIndex];
  }

  swipe(e: TouchEvent, when: string): void {
    const coord: [number, number] = [e.changedTouches[0].pageX, e.changedTouches[0].pageY];
    const time = new Date().getTime();

    if (when === 'start') {
      this.swipeCoord = coord;
      this.swipeTime = time;
    }

    else if (when === 'end') {
      const direction = [coord[0] - this.swipeCoord[0], coord[1] - this.swipeCoord[1]];
      const duration = time - this.swipeTime;

      if (duration < 1000 //Short enough
        && Math.abs(direction[1]) < Math.abs(direction[0]) //Horizontal enough
        && Math.abs(direction[0]) > 30) {  //Long enough
        const swipe = direction[0] < 0 ? 'next' : 'previous';
        if (swipe === 'next') {
          this.nextCode();
        } else {
          this.prevCode();
        }
      }
    }
  }

  prevCode() {
    if (this.codeIndex === 0) {
      return;
    } else {
      this.codeIndex--;
      this.code = this.workshop_groups[this.codeIndex];
    }
  }

  nextCode() {
    if (this.codeIndex === this.workshop_groups.length - 1) {
      return;
    } else {
      this.codeIndex++;
      this.code = this.workshop_groups[this.codeIndex];
    }
  }

  gotoCode(index) {
    this.code = this.track.codes[index];
    this.view_type = 'code';
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
