import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  updateRgbColor(color: string): Observable<any> {
    const options: any = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      })
    };
    const endpoint = `/rgb/color`;
    return this.http.put(endpoint, { color }, options);
  }
}
