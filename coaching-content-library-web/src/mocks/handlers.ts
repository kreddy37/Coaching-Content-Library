import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/v1/content', () => {
    return HttpResponse.json({
      data: {
        items: [
          {
            id: '1',
            title: 'Test Drill 1',
            description: 'Description for test drill 1',
            source: 'YouTube',
            url: 'https://youtube.com/watch?v=1',
            tags: ['test', 'drill'],
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ],
        total: 1,
        page: 1,
        size: 10,
        pages: 1,
      },
    });
  }),
];
