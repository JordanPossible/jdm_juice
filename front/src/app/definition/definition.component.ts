import { Component, OnInit , Input, AfterContentInit} from '@angular/core';
import { Definition } from './../models/definition';

@Component({
  selector: 'app-definition',
  templateUrl: './definition.component.html',
  styleUrls: ['./definition.component.scss']
})
export class DefinitionComponent implements OnInit {

  @Input() definition : Definition ;
  
  constructor() { }

  ngOnInit() {
  }

ngAfterContentInit(){

}
}
