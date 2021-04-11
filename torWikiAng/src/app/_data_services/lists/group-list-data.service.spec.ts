import { TestBed, inject } from '@angular/core/testing';

import { GroupListDataService } from './group-list-data.service';

describe('GroupListDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GroupListDataService]
    });
  });

  it('should be created', inject([GroupListDataService], (service: GroupListDataService) => {
    expect(service).toBeTruthy();
  }));
});
