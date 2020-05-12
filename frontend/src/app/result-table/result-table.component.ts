import { Component, OnInit, ViewChild, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import * as jsPDF from 'jspdf';
import 'jspdf-autotable';
import { CsvDataService } from '../csv-data.service';
@Component({
  selector: 'app-result-table',
  templateUrl: './result-table.component.html',
  styleUrls: ['./result-table.component.scss']
})

export class ResultTableComponent implements OnChanges {

  @Input()
  public course;

  @Input()
  public sem;

  @Input()
  public res_type;

  @Input()
  public list = [];

  displayedColumns = ['position', 'roll_no', 'name', 'sgpa', 'res_des', 'status'];
  dataSource;

  public passLabels = ['PASS', 'GRACE', 'FAIL'];
  public passData = [
    { data: [65, 49, 32], label: 'SGPA' }
  ];
  public passType = 'pie';

  public sgpaLabels = ['0 - 1', '1 - 2', '2 - 3', '3 - 4', '4 - 5', '5 - 6', '6 - 7', '7 - 8', '8 - 9', '9 - 10'];
  public sgpaData = [
    { data: [65, 49, 32, 32, 75, 90], label: 'SGPA' }
  ];
  public sgpaType = 'bar';



  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor() {
    this.updateData();
  }

  ngOnChanges(changes: SimpleChanges) {
    this.dataSource = new MatTableDataSource(this.list);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    this.updateData();
  }

  updateData() {
    let pass = 0, fail = 0, grace = 0;
    let sgpa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    this.list.forEach(e => {
      if (e.res_des.includes('GRACE')) {
        grace++;
      } else if (e.res_des.includes('Fail')) {
        fail++;
      } else {
        pass++;
      }

      sgpa[Math.floor(e.sgpa)]++;

    });

    this.passData = [
      { data: [pass, grace, fail], label: '' }
    ];

    this.sgpaData = [
      { data: sgpa, label: 'SGPA COUNT' }
    ];

  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  downloadCSV() {
    CsvDataService.exportToCsv(`result-${this.course}-${this.sem}-${this.res_type}.csv`, this.dataSource.filteredData);
  }

  downloadPDF() {
    let data = [];
    this.dataSource.filteredData.forEach(obj => {
      let arr = [];
      this.displayedColumns.forEach(col => {
        arr.push(obj[col]);
      });
      data.push(arr);
    });

    const doc = new jsPDF();
    doc.autoTable({
      head: [this.displayedColumns],
      body: data
    });
    doc.save(`result-${this.course}-${this.sem}-${this.res_type}.pdf`);
  }

}
