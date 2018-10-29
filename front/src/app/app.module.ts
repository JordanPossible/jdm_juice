import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
// my stuff
import { AppComponent } from './app.component';
import {MotsApiService} from './mots/mots-api.service';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { DefinitionComponent } from './definition/definition.component';
import { StatsComponent } from './stats/stats.component';
import { RelationComponent } from './relation/relation.component';


@NgModule({
  declarations: [
    AppComponent,
    DefinitionComponent,
    StatsComponent,
    RelationComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    MDBBootstrapModule.forRoot()
  ],
  providers: [MotsApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
