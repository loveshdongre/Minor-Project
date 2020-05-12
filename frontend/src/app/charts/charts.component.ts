import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements OnInit {

  options = {
    scaleShowVerticalLines: false,
    responsive: true,
  };

  @Input()
  labels = ['2006', '2007', '2008', '2009', '2010', '2012'];

  @Input()
  public data = [
    { data: [65, 49, 32, 32, 75, 90], label: 'SGPA' }
  ];

  @Input()
  chartType = 'bar';

  constructor() { }

  ngOnInit() {
  }

}
