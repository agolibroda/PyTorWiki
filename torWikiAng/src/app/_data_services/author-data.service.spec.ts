import { TestBed, inject } from '@angular/core/testing';

import { AuthorDataService } from './author-data.service';

describe('AuthorDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AuthorDataService]
    });
  });

  it('should be created', inject([AuthorDataService], (service: AuthorDataService) => {
    expect(service).toBeTruthy();
  }));
});
