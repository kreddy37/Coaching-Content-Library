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
            difficulty: 'Beginner',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
          {
            id: '2',
            title: 'Test Drill 2',
            description: 'Description for test drill 2',
            source: 'Reddit',
            url: 'https://reddit.com/r/test/comments/1',
            tags: ['test', 'drill'],
            difficulty: 'Intermediate',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
          {
            id: '3',
            title: 'Test Drill 3',
            description: 'Description for test drill 3',
            source: 'TikTok',
            url: 'https://tiktok.com/t/1',
            tags: ['test', 'drill'],
            difficulty: 'Advanced',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ],
        total: 3,
        page: 1,
        size: 10,
        pages: 1,
      },
    });
  }),
];
