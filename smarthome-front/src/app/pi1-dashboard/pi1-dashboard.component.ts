import {Component, OnInit} from '@angular/core';
import {Socket} from 'ngx-socket-io';
import {BuzzerService} from 'src/services/buzzer.service';

@Component({
  selector: 'app-pi1-dashboard',
  templateUrl: './pi1-dashboard.component.html',
  styleUrls: ['./pi1-dashboard.component.css']
})
export class Pi1DashboardComponent implements OnInit {

  dht1: UpdateDTO[] = [];
  dht2: UpdateDTO[] = [];
  dl: UpdateDTO = {} as UpdateDTO;
  uds1: UpdateDTO = {} as UpdateDTO;
  rpir1: UpdateDTO = {} as UpdateDTO;
  rpir2: UpdateDTO = {} as UpdateDTO;
  dpir1: UpdateDTO = {} as UpdateDTO;
  db: UpdateDTO = {} as UpdateDTO;
  ds1: UpdateDTO = {} as UpdateDTO;
  past1m: number = {} as number;
  past5m: number = {} as number;

  iframeBaseUrl = "http://localhost:3000/d-solo/b478d5b9-13b0-4b97-a14e-07ec4b5df704/new-dashboard?orgId=1";
  iframeUrls: string[] = [];

  constructor(private socket: Socket,
              private buzzerService: BuzzerService) {
  }

  ngOnInit(): void {
    this.buzzerService.receivedDoorBuzzerUpdate().subscribe({
      next: (value) => {
        let buzzerData: UpdateDTO = value;
        if (this.db.datetime != buzzerData.datetime)
          this.db = buzzerData
      },
      error(err) {
        console.log(err);
      },
    })
    this.socket.on('new-sensor-value/PI1', (data: any) => {
      data = JSON.parse(data);
      switch (data["name"]) {
        case "RDHT1" :
          this.updateDHT(data, this.dht1);
          break;
        case "RDHT2" :
          this.updateDHT(data, this.dht2);
          break;
        case "DL":
          this.dl = data;
          break;
        case "DUS1":
          this.uds1 = data;
          break;
        case "RPIR1":
          this.rpir1 = data;
          break;
        case "RPIR2":
          this.rpir2 = data;
          break;
        case "DPIR1":
          this.dpir1 = data;
          break;
        case "DB":
          this.db = data;
          break;
        case "DS1":
          this.ds1 = data;
          break;
      }
      //console.log('Received Socket.IO message:', data);
    });
  }


  // Function to calculate timestamp based on the relative time
  private calculateTimestamp(amount: number, unit: string): number {
    const currentDate = new Date();
    switch (unit) {
      case 'minutes':
        currentDate.setMinutes(currentDate.getMinutes() + amount);
        break;
      case 'hours':
        currentDate.setHours(currentDate.getHours() + amount);
        break;
      case 'days':
        currentDate.setDate(currentDate.getDate() + amount);
        break;
      case 'months':
        currentDate.setMonth(currentDate.getMonth() + amount);
        break;
    }
    return currentDate.getTime();
  }

  updateDHT(data: UpdateDTO, dht: UpdateDTO[]) {
    if (data["measurement"].toLowerCase() == "temperature") {
      dht[0] = data;
    } else {
      dht[1] = data;
    }
  }

    protected readonly parseFloat = parseFloat;
}

export interface UpdateDTO {
  measurement: string,
  simulated: boolean,
  runs_on: string,
  name: string,
  value: string,
  field: string,
  bucket: string,
  update_front: boolean,
  datetime: string,
  axis: string | undefined
}
