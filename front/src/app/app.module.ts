import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
// my stuff
import { AppComponent } from './app.component';
import {MotsApiService} from './mots/mots-api.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [MotsApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
