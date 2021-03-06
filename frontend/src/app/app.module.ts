import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import {EmailListDialogComponent} from './app.component';
import { TrackComponent } from './track/track.component';
import {TrackService} from './track.service';
import { TrackListComponent } from './track-list/track-list.component';
import {
  MatButtonModule, MatButtonToggleModule, MatIconModule, MatTooltipModule, MatMenuModule, MatToolbarModule, MatCardModule,
  MatInputModule, MatCheckboxModule, MatFormFieldModule, MatTabsModule, MatProgressSpinnerModule,
  MatExpansionModule, MatSelectModule, MatListModule, MatRadioModule, MatStepperModule, MatSidenavModule,
  MatDialogModule, MatDatepickerModule, MatNativeDateModule, MatSnackBar, MatSnackBarModule
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
import { SessionComponent } from './session/session.component';
import { ReviewComponent } from './review/review.component';
import { ReviewStarsComponent } from './review-stars/review-stars.component';
import { TimesPipe } from './times.pipe';
import {AccountDetailsComponent, NewUserDialogComponent} from './account-details/account-details.component';
import {AccountService} from './account.service';
import { AccountRedirectComponent } from './account-redirect/account-redirect.component';
import {AuthGuard} from './auth.guard';
import { SessionDashboardComponent } from './session-dashboard/session-dashboard.component';
import { SearchComponent } from './search/search.component';
import { TrackProgressComponent } from './track-progress/track-progress.component';
import {AccountFormComponent} from './account-form/account-form.component';
import { TrackFormComponent } from './track-form/track-form.component';
import { CodeFormComponent } from './code-form/code-form.component';
import {DndModule} from 'ng2-dnd';
import { ParticipantSearchComponent } from './participant-search/participant-search.component';
import { SessionFormComponent } from './session-form/session-form.component';
import {OverlayModule} from '@angular/cdk/overlay';
import { ParticipantFormComponent } from './participant-form/participant-form.component';
import {DatePipe} from '@angular/common';
import { PostComponent } from './post/post.component';
import {InfiniteScrollModule} from 'ngx-infinite-scroll';
import { SessionListComponent } from './session-list/session-list.component';
import { WorkshopDashboardComponent } from './workshop-dashboard/workshop-dashboard.component';
import { EmailFormComponent } from './email-form/email-form.component';
import { MarkdownToHtmlModule } from 'ng2-markdown-to-html';
import {
  ConfirmRegistrationDialogComponent,
  DeclineRegistrationDialogComponent, UnFollowDialogComponent, WorkshopDetailsComponent
} from './workshop-details/workshop-details.component';
import { AboutComponent } from './about/about.component';
import { HelpComponent } from './help/help.component';
import {HttpClientModule} from '@angular/common/http';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'find', redirectTo: 'search', data: {title: 'Search'}},
  {path: 'home', component: HomeComponent, data: {title: 'Home'}},
  {path: 'about', component: AboutComponent, data: {title: 'About'}},
  {path: 'help', component: HelpComponent, data: {title: 'Help'}},
  {path: 'search/:query', component: SearchComponent, data: {title: 'Search'}},
  {path: 'search', component: SearchComponent, data: {title: 'Search'}},
  {path: 'track/:id', component: TrackDetailsComponent, data: {title: 'Track'}},
  {path: 'track-form/:id', component: TrackFormComponent, data: {title: 'Create/Edit Track'}},
  {path: 'workshop-form/:id', component: WorkshopFormComponent, data: {title: 'Create/Edit Workshop'}},
  {path: 'participant-form/:id', component: ParticipantFormComponent, data: {title: 'Create/Edit Participants'}},
  {path: 'workshop/:id', component: WorkshopDetailsComponent, data: {title: 'Workshop'}},
  {path: 'workshop/:id/:action/:sessionId/:code', component: WorkshopDetailsComponent, data: {title: 'Workshop'}},
  {path: 'account/:token', component: AccountRedirectComponent, data: {title: 'Account Details'}},
  {path: 'accountDetails', component: AccountDetailsComponent, data: {title: 'Your Account'}, canActivate: [AuthGuard]},
  {path: 'sessionDashboard/:id', component: SessionDashboardComponent, canActivate: [AuthGuard]},
  {path: 'workshopDashboard/:id', component: WorkshopDashboardComponent, canActivate: [AuthGuard]}
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
    ReviewComponent,
    ReviewStarsComponent,
    TimesPipe,
    AccountDetailsComponent,
    AccountRedirectComponent,
    SessionDashboardComponent,
    SearchComponent,
    TrackProgressComponent,
    AccountFormComponent,
    TrackFormComponent,
    CodeFormComponent,
    ConfirmDialogComponent,
    ParticipantSearchComponent,
    SessionFormComponent,
    ParticipantFormComponent,
    PostComponent,
    SessionListComponent,
    WorkshopDashboardComponent,
    EmailFormComponent,
    ConfirmRegistrationDialogComponent,
    DeclineRegistrationDialogComponent,
    NewUserDialogComponent,
    UnFollowDialogComponent,
    EmailListDialogComponent,
    AboutComponent,
    HelpComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatTooltipModule,
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
    MatDatepickerModule,
    OverlayModule,
    MatNativeDateModule,
    InfiniteScrollModule,
    DndModule.forRoot(),
    RouterModule.forRoot(routes, {useHash: true}),
    MarkdownToHtmlModule.forRoot(),
    MatSnackBarModule
  ],
  entryComponents: [ConfirmDialogComponent,
    ConfirmRegistrationDialogComponent,
    DeclineRegistrationDialogComponent,
    NewUserDialogComponent,
    UnFollowDialogComponent,
    EmailListDialogComponent],
  providers: [TrackService, WorkshopService, ApiService, AccountService, AuthGuard, DatePipe],
  bootstrap: [AppComponent]
})


export class AppModule { }
