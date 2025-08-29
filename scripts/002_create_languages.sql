-- Create languages table for language/dialect tagging
CREATE TABLE IF NOT EXISTS public.languages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  native_name TEXT,
  iso_code TEXT,
  region TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.languages ENABLE ROW LEVEL SECURITY;

-- Allow everyone to read languages
CREATE POLICY "languages_select_all" ON public.languages FOR SELECT USING (true);

-- Insert some common Indian languages
INSERT INTO public.languages (name, native_name, iso_code, region) VALUES
('Hindi', 'हिन्दी', 'hi', 'North India'),
('Bengali', 'বাংলা', 'bn', 'East India'),
('Telugu', 'తెలుగు', 'te', 'South India'),
('Marathi', 'मराठी', 'mr', 'West India'),
('Tamil', 'தமிழ்', 'ta', 'South India'),
('Gujarati', 'ગુજરાતી', 'gu', 'West India'),
('Urdu', 'اردو', 'ur', 'North India'),
('Kannada', 'ಕನ್ನಡ', 'kn', 'South India'),
('Odia', 'ଓଡ଼ିଆ', 'or', 'East India'),
('Malayalam', 'മലയാളം', 'ml', 'South India'),
('Punjabi', 'ਪੰਜਾਬੀ', 'pa', 'North India'),
('Assamese', 'অসমীয়া', 'as', 'Northeast India'),
('English', 'English', 'en', 'Global')
ON CONFLICT (name) DO NOTHING;
