/**
 * Backend Contract Types
 *
 * CRITICAL: These types MUST match the backend API exactly.
 * See: project-context.md#Critical Backend Contract
 *
 * Field Names (snake_case - exact match required):
 * ✅ drill_tags, drill_description, content_type, published_at
 * ❌ NEVER: tags, description, contentType, publishedAt
 *
 * Enum Values (PascalCase - exact match required):
 * ✅ 'YouTube' | 'Reddit' | 'Instagram' | 'TikTok'
 * ❌ NEVER: 'youtube', 'YOUTUBE', 'Youtube'
 *
 * Null Handling:
 * ✅ Use | null for nullable fields (backend returns null, not undefined)
 * ❌ NEVER: | undefined
 */

export const ContentSource = {
  YouTube: 'YouTube',
  Reddit: 'Reddit',
  Instagram: 'Instagram',
  TikTok: 'TikTok',
} as const;

export type ContentSource = typeof ContentSource[keyof typeof ContentSource];

export const ContentType = {
  Video: 'Video',
  Stream: 'Stream',
  Post: 'Post',
  Short: 'Short',
} as const;

export type ContentType = typeof ContentType[keyof typeof ContentType];

export interface ContentItem {
  id: number;
  source: ContentSource;
  content_type: ContentType;
  url: string;
  title: string;
  author: string | null;
  thumbnail_url: string | null;
  drill_description: string | null;
  drill_tags: string[];
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced' | null;
  age_group: string | null;
  equipment: string | null;
  view_count: number | null;
  published_at: string | null;
  fetched_at: string;
  saved_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

export interface ContentListResponse {
  items: ContentItem[];
  total: number;
  limit: number;
  offset: number;
}
