import { Injectable } from '@angular/core';
import { concatMap, delay, iif, Observable, of, retry, retryWhen, tap, throwError } from 'rxjs';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { environment } from '../environments/environment';

@Injectable({
 providedIn: 'root',
})
export class WebSocketService {
  subject: WebSocketSubject<string>;
  disconnected = false;

  constructor() {
    this.subject = webSocket<string>({
      url: environment.wsUrl,
      deserializer: ({data}) => data,
      serializer: msg => msg      
    });

    this.subject.asObservable().pipe(
      retry({ delay: errors =>
        errors.pipe(
          concatMap((error, i) =>
            iif(
              () => environment.webSockets.maxReconnectAttempts !== -1 &&
                i >= environment.webSockets.maxReconnectAttempts,
              throwError(() => new Error('WebSocket reconnecting retry limit exceeded!')),
              of(error).pipe(
                tap(() => {
                  this.disconnected = true;
                  console.log('Trying to reconnect to WebSocket server...');
                }),
                delay(environment.webSockets.reconnectAttemptDelay)
              )
            )
          )
        )
      }),
      tap(() => {
        if (this.disconnected) {
          this.disconnected = false;
          console.log('Successfully re-connected to the WebSocket server.');
        }
      })
    ).subscribe(
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