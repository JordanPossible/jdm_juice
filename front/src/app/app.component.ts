import { Component, OnInit, OnDestroy } from '@angular/core';
import { MotsApiService } from './mots/mots-api.service';
import { Definition } from './models/definition';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})



export class AppComponent implements OnInit, OnDestroy {

  title = 'app';

  json_Res : any;

  definition : Definition;

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

        this.json_Res = res;

        // console.log(res)
        this.definition = {
        id: 1,
        title: word,
        body: this.json_Res.definition
      };
        //this.json_Res = res;
      });
  }


  ngOnDestroy() {
    // this.result_box.unsubscribe();
  }



}
