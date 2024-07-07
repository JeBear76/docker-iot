import { Routes } from '@angular/router';
import { IotListenerComponent } from './iot-listener/iot-listener.component';

export const routes: Routes = [
    { path: 'iot-listener', component: IotListenerComponent },
    { path: '**', redirectTo: 'iot-listener' }
];
