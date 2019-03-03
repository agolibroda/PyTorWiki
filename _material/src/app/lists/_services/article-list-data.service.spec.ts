import { TestBed, inject } from '@angular/core/testing';

import { ArticleListDataService } from './article-list-data.service';

describe('ArticleListDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ArticleListDataService]
    });
  });

  it('should be created', inject([ArticleListDataService], (service: ArticleListDataService) => {
    expect(service).toBeTruthy();
  }));
});
