import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";

@Injectable({
 providedIn: 'root',
})
export class WebSocketService {
  subject: WebSocketSubject<string>;
  
  constructor() {
    this.subject = webSocket<string>({
      url: 'ws://localhost:8000',
      deserializer: ({data}) => data,
      serializer: msg => msg
      
    });

    this.subject.asObservable().subscribe(
      {
        next: (msg:string) => { 
          console.log('message received: ' + msg);
        },
        error: (err) => console.log(err),
        complete: () => console.log('complete')
      }
    );

    
  }

  linkToSocket() : Observable<string> {
    return this.subject.asObservable();
  }
 
}