import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import {UserAndTokenService} from '../user.token.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.css'],
  //providers: [UserAndTokenService]  
})
export class LoginFormComponent implements OnInit{
  title = 'app';
  registrationForm: FormGroup;
  isValid: boolean=false;
  
  constructor(private fb: FormBuilder,private http: HttpClient, private userAndToken: UserAndTokenService, private route: Router) { // <--- inject FormBuilder
    this.createForm();   
  }

  ngOnInit() {
  }

  createForm() {
    this.registrationForm = this.fb.group({
 
      email: ['',Validators.required],
      password: ['',Validators.required]
      //repassword: ['',Validators.required]
    });
  
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
    //console.log(formVal); 
    this.http.post('http://34.210.127.92:8000/login/', formVal, {headers: new HttpHeaders().set('Content-Type', 'application/json'),}).subscribe(
      resp => {console.log(resp);
        this.userAndToken.setUserAndToken(resp["token"]);

        
          this.route.navigate(['/mainpage']);
        
  });
  	}else{
		alert("Please fill the form correctly."); 
  	}
  }
}