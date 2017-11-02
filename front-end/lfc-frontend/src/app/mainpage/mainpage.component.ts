import { Component, OnInit } from '@angular/core';
import {HttpClient,HttpHeaders} from '@angular/common/http';

@Component({
  selector: 'app-mainpage',
  templateUrl: './mainpage.component.html',
  styleUrls: ['./mainpage.component.css']
})
export class MainpageComponent implements OnInit {
  isValid: boolean=false;
  concert: any;
  constructor(private http: HttpClient) {
    this.http.get('http://34.210.127.92:8000/concerts/').subscribe( data => {
      this.concert=data;
    });
   }

  ngOnInit() {
  }

}
