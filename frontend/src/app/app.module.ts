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
import {WorkshopService} from "./workshop.service";
import { WorkshopComponent } from './workshop/workshop.component';
import { WorkshopListComponent } from './workshop-list/workshop-list.component';
import { FlexLayoutModule } from "@angular/flex-layout";
import { WorkshopFormComponent } from './workshop-form/workshop-form.component';
import {ApiService} from "./api.service";

@NgModule({
  declarations: [
    AppComponent,
    TrackComponent,
    TrackListComponent,
    WorkshopComponent,
    WorkshopListComponent,
    WorkshopFormComponent
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
    MdFormFieldModule
  ],
  providers: [TrackService, WorkshopService, ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
