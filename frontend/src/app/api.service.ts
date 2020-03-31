import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})

export class ApiService {

  url = 'http://localhost:8000/app/students/';
  constructor(private http: HttpClient) { }

  getResult(reqData) {
    return this.http.post<any>(this.url, reqData);
  }

}
