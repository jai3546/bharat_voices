import { StorySubmissionForm } from "@/components/story-submission-form"

export default function ShareStoryPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-red-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-orange-900 mb-4">Share Your Story</h1>
          <p className="text-lg text-orange-700">Share your cultural stories, proverbs, and wisdom with the world</p>
        </div>
        <StorySubmissionForm />
      </div>
    </div>
  )
}
