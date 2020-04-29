import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class ApiService {

  resultUrl = 'http://localhost:8000/app/students/';

  loginUrl = 'http://localhost:8000/app/login/';

  generateUrl = 'http://localhost:8000/app/generate/';

  logoutUrl = 'http://localhost:8000/app/logout/';

  constructor(private http: HttpClient) { }

  getResult(reqData) {
    return this.http.post<any>(this.resultUrl, reqData);
  }

  login(reqData) {
    return this.http.post<any>(this.loginUrl, reqData);
  }

  generateResult(reqData, token) {
    const headers = new HttpHeaders().set('Authorization', `token ${token}`);
    return this.http.post<any>(this.generateUrl, reqData, { headers });
  }

  logout(token) {
    const headers = new HttpHeaders().set('Authorization', `token ${token}`);
    return this.http.get<any>(this.logoutUrl, { headers });
  }

}
