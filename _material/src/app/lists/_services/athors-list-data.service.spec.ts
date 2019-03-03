import { TestBed, inject } from '@angular/core/testing';

import { AthorsListDataService } from './athors-list-data.service';

describe('AthorsListDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AthorsListDataService]
    });
  });

  it('should be created', inject([AthorsListDataService], (service: AthorsListDataService) => {
    expect(service).toBeTruthy();
  }));
});
