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

  @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: true }) sort: MatSort;

  constructor() { }

  ngOnChanges(changes: SimpleChanges) {
    this.dataSource = new MatTableDataSource(this.list);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
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

    console.log(this.dataSource);
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
