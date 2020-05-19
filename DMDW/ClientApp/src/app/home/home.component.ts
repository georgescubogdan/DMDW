import { Component, Inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ThrowStmt } from '@angular/compiler';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  public url: string = '';
  public response: any;
  baseURL: string;
  showBars = false;
  topics = [];
  topicNames = [
    "Clothes",
    "Sport",
    "-",
    "People",
    "-",
    "-",
    "Medical/Viruses",
    "Blogs",
    "Food",
    "Articles",
  ]
  types = [
    "success",
    "info",
    "danger",
    "primary",
    "warning",
    "dark",
    "secondary",
  ]

  type(i: number) : string {
    let x = (i + 1) * Date.now();
    
    // console.log(i);
    
    return this.types[(x) % 7];
  }
  constructor(public http: HttpClient, @Inject('BASE_URL') baseUrl: string) {
    this.baseURL = baseUrl;  
  }

  submit() {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    this.http.post<any>(this.baseURL + 'api/Data', '\"' + this.url + '\"', { headers }).subscribe(result => {
      this.response = result;
      console.log(result);
      this.showBars = false;
      
    }, error => console.error(error));
  }

  show() {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    this.http.get<any>(this.baseURL + 'api/Data', { headers }).subscribe(result => {
      // this.response = result;
      // console.log(result);
      this.topics = [];
      for (let i = 1; i <= 10; i++) {
        this.topics.push(result[i] * 100);

      }
      this.showBars = true;
    }, error => console.error(error));
  }

}
