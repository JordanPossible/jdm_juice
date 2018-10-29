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
  liste_type : any;

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

            console.log(res);

            this.definition = {
              title: word,
              body: []
            };

            this.liste_type = {
              relations: []
            }

            var regExp =/\(([^)]+)\)/g;
            var regExp2 =/[0-9]\./g
            //Changer par un array dans le JSON 
            for(let types_r in this.json_Res.rels_types_dico) {
              this.liste_type.relations.push(types_r[0]);
              console.log(this.json_Res.rels_types_dico.0);

            }

            for(var i in this.json_Res.definition) {

                var item = this.json_Res.definition[i];
                var matches = item.match(regExp);
                this.definition.body.push({
                    "id" : item.charAt(0),
                    "body" : item.replace(regExp2, ''),
                    "fam" : []
                });
                for(var j in matches) {
                    var par = matches[j].replace('(', '').replace(')','');
                    this.definition.body[i].fam.push(par);
                }

            }

        //this.json_Res = res;
      });
  }


  ngOnDestroy() {
    // this.result_box.unsubscribe();
  }



}
