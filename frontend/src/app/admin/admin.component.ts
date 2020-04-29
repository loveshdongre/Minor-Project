import { ApiService } from './../api.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormsModule } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { DialogComponent } from '../dialog/dialog.component';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
})
export class AdminComponent implements OnInit {

  loginForm: FormGroup;
  resultForm: FormGroup;
  free = true;


  constructor(private fb: FormBuilder, private apiService: ApiService, public dialog: MatDialog) { }

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
    this.openDialog();
    this.free = false;
    this.apiService.generateResult(this.resultForm.value, this.getToken()).subscribe(
      response => {
        console.log('Request Successful');
        this.free = true;
      },
      error => {
        console.log('error', error)
        this.free = true;
      }
    );
  }

  loggedIn() {
    return !!this.getToken();
  }

  public getToken() {
    return localStorage.getItem('token');
  }

  public removeToken() {
    return localStorage.removeItem('token');
  }

  logout(): void {

    this.apiService.logout(this.getToken()).subscribe(
      response => {
        this.removeToken();
        console.log('logout');
      },
      error => {
        console.log('logout failed');
      }
    );
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogComponent, {
      width: '250px'
    });
  }

}
