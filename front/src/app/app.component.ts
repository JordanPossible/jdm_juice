import { Component, OnInit, OnDestroy } from '@angular/core';
import { MotsApiService } from './mots/mots-api.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})



export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  result_box: any;
  word: string;
  selected : string;
  typeSearch = ["type1", "type2", "type3", "type4", "type5",
         "type6", "type7", "type8", "type9"];

  constructor(private motsApi: MotsApiService) {

  }


  ngOnInit() {
    this.selected="type2";
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
