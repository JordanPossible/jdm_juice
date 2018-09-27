import { Component, OnInit, OnDestroy } from '@angular/core';
import { MotsApiService } from './mots/mots-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  result_box: any;
  word: string;

  constructor(private motsApi: MotsApiService) {
  }

  ngOnInit() {
  }

  callApi(word) {
    // console.log(word)
    this.motsApi
      .getMots(word)
      .subscribe(res => {
        // console.log(res)
        this.result_box = res;
      });
  }

  ngOnDestroy() {
    // this.result_box.unsubscribe();
  }
}
