-- Create badges table for gamification
CREATE TABLE IF NOT EXISTS public.badges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL,
  icon TEXT,
  color TEXT DEFAULT '#6366f1',
  requirement_type TEXT NOT NULL CHECK (requirement_type IN ('contributions', 'likes_received', 'streak', 'languages', 'categories')),
  requirement_value INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.badges ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read badges
CREATE POLICY "badges_select_all" ON public.badges FOR SELECT USING (true);

-- Insert default badges
INSERT INTO public.badges (name, description, icon, color, requirement_type, requirement_value) VALUES
('First Story', 'Share your first story or proverb', '🌟', '#f59e0b', 'contributions', 1),
('Storyteller', 'Share 5 stories or proverbs', '📚', '#8b5cf6', 'contributions', 5),
('Cultural Ambassador', 'Share 25 stories or proverbs', '🏆', '#ef4444', 'contributions', 25),
('Community Favorite', 'Receive 10 likes on your stories', '❤️', '#ec4899', 'likes_received', 10),
('Beloved Narrator', 'Receive 50 likes on your stories', '💖', '#f97316', 'likes_received', 50),
('Consistent Contributor', 'Maintain a 7-day contribution streak', '🔥', '#10b981', 'streak', 7),
('Dedicated Storyteller', 'Maintain a 30-day contribution streak', '⚡', '#06b6d4', 'streak', 30),
('Multilingual', 'Share stories in 3 different languages', '🌍', '#84cc16', 'languages', 3),
('Cultural Explorer', 'Share stories across 5 different categories', '🗺️', '#a855f7', 'categories', 5)
ON CONFLICT (name) DO NOTHING;
