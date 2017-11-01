import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  moduleId: module.id
})

export class ListConcerts {
  title = 'List Concert';
  
  isValid: boolean=false;
  concert: any;

  constructor(private fb: FormBuilder,private http: HttpClient) { 
    this.http.get('http://34.210.127.92:8000/concerts/').subscribe( data => {
      this.concert=data;
    });
    
  }


 
}




