import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
@Component({
  selector: 'app-create-concert',
  templateUrl: './create-concert.component.html',
  styleUrls: ['./create-concert.component.css']
})
export class CreateConcertComponent implements OnInit {
  title = 'app';
  concertForm: FormGroup;
  isValid: boolean=false;
  
  constructor(private fb: FormBuilder,private http: HttpClient) { // <--- inject FormBuilder
    this.createForm();   
  }

  createForm() {
    this.concertForm = this.fb.group({
      name: ['',Validators.required], // <--- the FormControl called "name"
      artist: ['',Validators.required],
      //location: '',
      date_time: ['',Validators.required],
      price_min: ['',Validators.required],
      price_max: ['',Validators.required],
      tags: this.fb.array([]),
    });
    
  }
  ngOnInit() {
  }
  get tags(): FormArray {
    return this.concertForm.get('tags') as FormArray;
  }
  addTag(){
    this.tags.push(new FormControl("",Validators.required));
  }
  deleteTag(i){
    this.tags.removeAt(i);
  }
  createConcert()
  {	
	this.isValid=true;	
	if(this.concertForm.valid){	
    let formVal=JSON.stringify(this.concertForm.value); 
    let header = new HttpHeaders().set('Content-Type', 'application/json');
    //header = header.append('Authorization', 'Token ' +this.userAndToken.getUserAndToken());
		this.http.post('http://localhost:8000/concert/', formVal, {headers: new HttpHeaders().set('Content-Type', 'application/json'),}).subscribe();
  	}else{
		alert("Please fill the form correctly."); 
  	}
  }
}
