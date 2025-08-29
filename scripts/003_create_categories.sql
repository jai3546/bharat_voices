-- Create categories table for themes
CREATE TABLE IF NOT EXISTS public.categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  color TEXT DEFAULT '#6366f1',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read categories
CREATE POLICY "categories_select_all" ON public.categories FOR SELECT USING (true);

-- Insert default categories
INSERT INTO public.categories (name, description, color) VALUES
('Wisdom', 'Traditional wisdom and life lessons', '#8b5cf6'),
('Family', 'Stories about family bonds and relationships', '#f59e0b'),
('Nature', 'Tales connected to nature and environment', '#10b981'),
('Courage', 'Stories of bravery and heroism', '#ef4444'),
('Love', 'Romantic tales and stories of affection', '#ec4899'),
('Humor', 'Funny stories and witty sayings', '#f97316'),
('Spirituality', 'Religious and spiritual narratives', '#6366f1'),
('Work', 'Stories about labor, craftsmanship, and dedication', '#84cc16'),
('Community', 'Tales of unity and social bonds', '#06b6d4'),
('Tradition', 'Cultural customs and traditional practices', '#a855f7')
ON CONFLICT (name) DO NOTHING;
