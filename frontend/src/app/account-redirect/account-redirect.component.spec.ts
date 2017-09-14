import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountRedirectComponent } from './account-redirect.component';

describe('AccountRedirectComponent', () => {
  let component: AccountRedirectComponent;
  let fixture: ComponentFixture<AccountRedirectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AccountRedirectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountRedirectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
