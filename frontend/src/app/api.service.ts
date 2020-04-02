import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class ApiService {

  result_url = 'http://localhost:8000/app/students/';

  login_url = 'http://localhost:8000/app/login/';

  generate_url = 'http://localhost:8000/app/generate/';

  constructor(private http: HttpClient) { }

  getResult(reqData) {
    return this.http.post<any>(this.result_url, reqData);
  }

  login(reqData) {
    return this.http.post<any>(this.login_url, reqData);
  }

  generateResult(reqData, token) {
    const headers = new HttpHeaders().set('Authorization', `token ${token}`);
    return this.http.post<any>(this.generate_url, reqData, { headers });
  }

}
