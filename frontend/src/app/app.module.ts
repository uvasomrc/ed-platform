import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TrackComponent } from './track/track.component';
import {TrackService} from './track.service';
import { TrackListComponent } from './track-list/track-list.component';
import {
  MatButtonModule, MatIconModule, MatMenuModule, MatToolbarModule, MatCardModule,
  MatInputModule, MatCheckboxModule, MatFormFieldModule, MatTabsModule, MatProgressSpinnerModule,
  MatExpansionModule, MatSelectModule, MatListModule, MatRadioModule, MatStepperModule, MatSidenavModule,
  MatDialogModule
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
import {ConfirmDialogComponent, TrackDetailsComponent} from './track-details/track-details.component';
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
import { TeacherDashboardComponent } from './teacher-dashboard/teacher-dashboard.component';
import { SearchComponent } from './search/search.component';
import { TrackProgressComponent } from './track-progress/track-progress.component';
import {AccountFormComponent} from './account-form/account-form.component';
import { TrackFormComponent } from './track-form/track-form.component';
import { CodeFormComponent } from './code-form/code-form.component';
import {DndModule} from 'ng2-dnd';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'find', redirectTo: 'search', data: {title: 'Search'}},
  {path: 'home', component: HomeComponent, data: {title: 'Home'}},
  {path: 'search', component: SearchComponent, data: {title: 'Search'}},
  {path: 'track/:id', component: TrackDetailsComponent, data: {title: 'Track'}},
  {path: 'track-form/:id', component: TrackFormComponent, data: {title: 'Create/Edit Track'}},
  {path: 'workshop-form/:id', component: WorkshopFormComponent, data: {title: 'Create/Edit Workshop'}},
  {path: 'workshop/:id', component: WorkshopDetailsComponent, data: {title: 'Workshop'}},
  {path: 'account/:token', component: AccountRedirectComponent, data: {title: 'Account Details'}},
  {path: 'accountDetails', component: AccountDetailsComponent, data: {title: 'Your Account'},
    canActivate: [AuthGuard]},
  {path: 'teacherDashboard/:id', component: TeacherDashboardComponent,
    canActivate: [AuthGuard]}
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
    TeacherDashboardComponent,
    SearchComponent,
    TrackProgressComponent,
    AccountFormComponent,
    TrackFormComponent,
    CodeFormComponent,
    ConfirmDialogComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatMenuModule,
    MatToolbarModule,
    MatIconModule,
    MatCardModule,
    FlexLayoutModule,
    MatInputModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatTabsModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatExpansionModule,
    MatListModule,
    MatRadioModule,
    MatStepperModule,
    MatSidenavModule,
    MatDialogModule,
    DndModule.forRoot(),
    RouterModule.forRoot(routes, {useHash: true})
  ],
  entryComponents: [ConfirmDialogComponent],
  providers: [TrackService, WorkshopService, ApiService, AccountService, AuthGuard],
  bootstrap: [AppComponent]
})

export class AppModule { }
