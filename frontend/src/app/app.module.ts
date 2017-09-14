import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TrackComponent } from './track/track.component';
import {TrackService} from './track.service';
import { TrackListComponent } from './track-list/track-list.component';
import {
  MdButtonModule, MdIconModule, MdMenuModule, MdToolbarModule, MdCardModule,
  MdInputModule, MdCheckboxModule, MdFormFieldModule, MdTabsModule
} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {WorkshopService} from './workshop.service';
import { WorkshopComponent } from './workshop/workshop.component';
import { WorkshopListComponent } from './workshop-list/workshop-list.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { WorkshopFormComponent } from './workshop-form/workshop-form.component';
import {ApiService} from './api.service';
import {RouterModule, Routes} from '@angular/router';
import { HomeComponent } from './home/home.component';
import { TrackDetailsComponent } from './track-details/track-details.component';
import { WorkshopDetailsComponent } from './workshop-details/workshop-details.component';
import { SessionComponent } from './session/session.component';
import { ParticipantBriefComponent } from './participant-brief/participant-brief.component';
import { ReviewComponent } from './review/review.component';
import { ReviewStarsComponent } from './review-stars/review-stars.component';
import { TimesPipe } from './times.pipe';
import { AccountDetailsComponent } from './account-details/account-details.component';
import {AccountService} from './account.service';
import { AccountRedirectComponent } from './account-redirect/account-redirect.component';
import {AuthGuard} from './auth.guard';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'find', redirectTo: 'search'},
  {path: 'home', component: HomeComponent},
  {path: 'track/:id', component: TrackDetailsComponent},
  {path: 'workshop/:id', component: WorkshopDetailsComponent},
  {path: 'account/:token', component: AccountRedirectComponent},
  {path: 'accountDetails', component: AccountDetailsComponent,
    canActivate: [AuthGuard]}
//  {path: 'track', component: TrackComponent},
// {path: 'workshop', component: WorkshopComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    TrackComponent,
    TrackListComponent,
    WorkshopComponent,
    WorkshopListComponent,
    WorkshopFormComponent,
    HomeComponent,
    TrackDetailsComponent,
    WorkshopDetailsComponent,
    SessionComponent,
    ParticipantBriefComponent,
    ReviewComponent,
    ReviewStarsComponent,
    TimesPipe,
    AccountDetailsComponent,
    AccountRedirectComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    BrowserAnimationsModule,
    MdButtonModule,
    MdMenuModule,
    MdToolbarModule,
    MdIconModule,
    MdCardModule,
    FlexLayoutModule,
    MdInputModule,
    MdCheckboxModule,
    MdFormFieldModule,
    MdTabsModule,
    RouterModule.forRoot(routes, {useHash: true})
  ],
  providers: [TrackService, WorkshopService, ApiService, AccountService, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
