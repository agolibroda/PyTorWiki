import { TestBed, inject } from '@angular/core/testing';

import { GroupDataService } from './group-data.service';

describe('GroupDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GroupDataService]
    });
  });

  it('should be created', inject([GroupDataService], (service: GroupDataService) => {
    expect(service).toBeTruthy();
  }));
});
