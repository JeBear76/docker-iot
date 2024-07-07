import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { WebSocketService } from '../websocket.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-iot-listener',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ],
  templateUrl: './iot-listener.component.html',
  styleUrl: './iot-listener.component.css'
})
export class IotListenerComponent{
  /**
   *
   */
  messages: string[] = [];
  newMessage: string = "";
  constructor(private websocketService: WebSocketService) { 
    websocketService.linkToSocket().subscribe({
      next: (msg:string) => { 
        console.log('message received: ' + msg);
        this.messages.push(msg);
      },
      error: (err) => console.log(err),
      complete: () => console.log('complete')
    });
  }

  sendMessage() {
    this.websocketService.subject.next(this.newMessage);
  }

}
