import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { TrackComponent } from './track/track.component';
import {TrackService} from './track.service';
import { TrackListComponent } from './track-list/track-list.component';
import {MdButtonModule, MdIconModule, MdMenuModule, MdToolbarModule, MdCardModule,
        MdInputModule, MdCheckboxModule, MdFormFieldModule} from '@angular/material';
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

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full'},
  {path: 'find', redirectTo: 'search'},
  {path: 'home', component: HomeComponent},
  {path: 'track/:id', component: TrackDetailsComponent}
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
    TrackDetailsComponent
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
    RouterModule.forRoot(routes, {useHash: true})
  ],
  providers: [TrackService, WorkshopService, ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
