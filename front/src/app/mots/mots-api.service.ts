import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {API_URL} from '../env';

@Injectable()
export class MotsApiService {

  constructor(private http: HttpClient) {
  }

  // GET list of public, future events
  getMots(word) {
    // console.log(`${API_URL}/mots/${word}`)
    return this.http
      .get(`${API_URL}/mots/${word}`, {responseType: 'text'})
  }
}
