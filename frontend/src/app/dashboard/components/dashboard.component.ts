import { Component, OnInit, ViewChild, ElementRef, AfterContentInit, HostListener, ViewContainerRef, TemplateRef } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styles: [`
  .content {
    background: #fff;
    padding: 24px;
    min-height: 280px
  }
  `]
})
export class DashboardComponent implements OnInit, AfterContentInit {
  @ViewChild('testElem')
  public testElem: ElementRef;

  constructor(private viewRef: ViewContainerRef) {

  }

  ngOnInit(): void {
    console.log('ngOnInit');
  }

  ngAfterContentInit(): void {
    console.log('ngAfterContentInit');
    console.log(this.testElem);
    console.log(this.viewRef);
    // this.testElem.nativeElement.style="background: red";
  }

  @HostListener('click', ['$event.target'])
  onClick(btn) {
    console.log('button', btn, 'number of clicks');
  }
}
