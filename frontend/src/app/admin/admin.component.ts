import { ApiService } from './../api.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormsModule } from '@angular/forms';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  loginForm: FormGroup;
  resultForm: FormGroup;


  constructor(private fb: FormBuilder, private apiService: ApiService) { }

  ngOnInit() {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(5)]],
      password: ['', [Validators.required, Validators.minLength(5)]]
    });

    this.resultForm = this.fb.group({
      res_type: ['M'],
      course: ['BTECH', [Validators.required]],
      sem: ['5', [Validators.required, Validators.min(1), Validators.max(8), Validators.maxLength(1)]],
      roll_no: ['0101CS171001', Validators.required],
      no: ['3', [Validators.required, Validators.min(1), Validators.maxLength(3)]]
    });

  }

  get password() {
    return this.loginForm.get('password');
  }

  get username() {
    return this.loginForm.get('username');
  }

  // form 2
  get res_type() {
    return this.resultForm.get('res_type');
  }

  get course() {
    return this.resultForm.get('course');
  }

  get sem() {
    return this.resultForm.get('sem');
  }

  get roll_no() {
    return this.resultForm.get('roll_no');
  }

  get no() {
    return this.resultForm.get('no');
  }

  onSubmit(): void {
    this.apiService.login(this.loginForm.value).subscribe(
      response => {
        localStorage.setItem('token', response.token);
        // console.log(response.token);
      },
      error => console.log('error', error)
    );
  }

  generate(): void {

    this.apiService.generateResult(this.resultForm.value, this.getToken()).subscribe(
      response => {
        console.log('Request Successful');
      },
      error => console.log('error', error)
    );
  }

  loggedIn() {
    return !!this.getToken();
  }

  public getToken() {
    return localStorage.getItem('token');
  }

}
