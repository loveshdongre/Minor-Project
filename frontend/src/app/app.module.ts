import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { MaterialModule } from './material/material.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';

import { NavbarComponent } from './navbar/navbar.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { ResultComponent } from './result/result.component';
import { ResultTableComponent } from './result-table/result-table.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { ApiService } from './api.service';
import { AdminComponent } from './admin/admin.component';
import { DialogComponent } from './dialog/dialog.component';
import { CsvDataService } from './csv-data.service';
import { ChartsComponent } from './charts/charts.component';

import { ChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    AboutComponent,
    ContactComponent,
    ResultComponent,
    ResultTableComponent,
    AdminComponent,
    DialogComponent,
    ChartsComponent,
  ],
  entryComponents: [DialogComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    LayoutModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ChartsModule
  ],
  schemas: [],
  providers: [ApiService, CsvDataService], // registering service
  bootstrap: [AppComponent],
})
export class AppModule { }
