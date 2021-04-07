import { TestBed, inject } from '@angular/core/testing';

import { ArticleDataService } from './article-data.service';

describe('ArticleDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ArticleDataService]
    });
  });

  it('should be created', inject([ArticleDataService], (service: ArticleDataService) => {
    expect(service).toBeTruthy();
  }));
});
