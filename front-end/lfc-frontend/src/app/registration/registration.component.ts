import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  title = 'app';
  registrationForm: FormGroup;
  isValid: boolean=false;
  
  constructor(private fb: FormBuilder,private http: HttpClient, private route: Router) { // <--- inject FormBuilder
    this.createForm();   
  }

  createForm() {
    this.registrationForm = this.fb.group({
      first_name: ['',Validators.required],
      last_name: ['',Validators.required],
      age: ['',Validators.required],
      email: ['',Validators.required],
      password: ['',Validators.required],
      comments: this.fb.array([]),
      //repassword: ['',Validators.required]
    });
  
  }

    
  ngOnInit() {
  }
  // customValidator() {         
  //   if(this.password ==   repassword) {
  //     this.isValid=true;
  //   } else {
  //     this.isValid=false;
  //   }
  // }

  register()
  {	

	this.isValid=true;	
	if(this.registrationForm.valid){	
    let formVal=JSON.stringify(this.registrationForm.value);
    console.log(formVal); 
		this.http.post('http://34.210.127.92:8000/signup/', formVal, {headers: new HttpHeaders().set('Content-Type', 'application/json'),}).subscribe(resp => {console.log(resp)});
    this.route.navigate(['/login']);  

    }else{
		alert("Please fill the form correctly."); 
  	}
  }
}