"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Heart, Share2, User, Calendar, Globe, Crown, Trophy, Award, Star, Plus } from "lucide-react"
import Link from "next/link"
import { useLanguage } from "@/lib/language-context"

// Dummy data for the community page
const featuredStory = {
  id: "featured-1",
  title: "The Wise Elephant and the Ant",
  content:
    "In the heart of Kerala, there lived a wise elephant named Ganesha who learned humility from a tiny ant. This ancient tale teaches us that wisdom comes in all sizes, and even the mightiest can learn from the smallest...",
  author: "Priya Nair",
  category: "Folk Tale",
  language: "Malayalam",
  likes: 247,
  shares: 89,
  date: "2024-01-15",
}

const communityStories = [
  {
    id: "1",
    title: "Vasudhaiva Kutumbakam",
    content:
      "The world is one family - this Sanskrit phrase from the Maha Upanishad reminds us that all of humanity is connected. In times of division, this ancient wisdom calls us to see beyond borders...",
    author: "Rajesh Kumar",
    category: "Philosophy",
    language: "Sanskrit",
    likes: 156,
    shares: 34,
    date: "2024-01-14",
    type: "proverb",
  },
  {
    id: "2",
    title: "The Generous Baker of Lahore",
    content:
      "My grandmother told me about a baker in old Lahore who would leave fresh bread outside his shop every morning for those who couldn't afford it. 'Neki kar darya mein daal' - do good and throw it in the river...",
    author: "Fatima Sheikh",
    category: "Kindness",
    language: "Urdu",
    likes: 203,
    shares: 67,
    date: "2024-01-13",
    type: "story",
  },
  {
    id: "3",
    title: "Ubuntu - I Am Because We Are",
    content:
      "This beautiful African philosophy teaches us that our humanity is interconnected. Ubuntu reminds us that we cannot exist in isolation - our well-being is tied to the well-being of others...",
    author: "Amara Okafor",
    category: "Philosophy",
    language: "Zulu",
    likes: 189,
    shares: 45,
    date: "2024-01-12",
    type: "saying",
  },
  {
    id: "4",
    title: "The Bamboo and the Storm",
    content:
      "A Japanese tale tells of bamboo that bends with the storm while mighty oaks break. 'Nana korobi ya oki' - fall seven times, rise eight. Resilience is not about being unbreakable...",
    author: "Hiroshi Tanaka",
    category: "Resilience",
    language: "Japanese",
    likes: 134,
    shares: 28,
    date: "2024-01-11",
    type: "folk_tale",
  },
]

const leaderboard = [
  { name: "Priya Nair", stories: 23, likes: 1247, badge: "Cultural Ambassador" },
  { name: "Rajesh Kumar", stories: 18, likes: 892, badge: "Wisdom Keeper" },
  { name: "Fatima Sheikh", stories: 15, likes: 756, badge: "Story Weaver" },
]

const badges = [
  { name: "First Story", description: "Share your first cultural story", icon: "🌟", earned: true },
  { name: "Wisdom Keeper", description: "Share 10 proverbs or sayings", icon: "📚", earned: true },
  { name: "Cultural Ambassador", description: "Get 100 likes on your stories", icon: "🌍", earned: false },
  { name: "Story Weaver", description: "Share stories in 3 different languages", icon: "🧵", earned: false },
  { name: "Community Favorite", description: "Have a story featured", icon: "❤️", earned: false },
  { name: "Voice of Heritage", description: "Share 5 audio stories", icon: "🎙️", earned: false },
]

export default function CommunityPage() {
  const [activeTab, setActiveTab] = useState("latest")
  const [likedStories, setLikedStories] = useState<Set<string>>(new Set())
  const { t } = useLanguage()

  const handleLike = (storyId: string) => {
    setLikedStories((prev) => {
      const newSet = new Set(prev)
      if (newSet.has(storyId)) {
        newSet.delete(storyId)
      } else {
        newSet.add(storyId)
      }
      return newSet
    })
  }

  const StoryCard = ({ story, featured = false }: { story: any; featured?: boolean }) => (
    <Card
      className={`border-orange-200 hover:shadow-lg transition-all duration-200 ${featured ? "border-2 border-amber-300 bg-gradient-to-r from-amber-50 to-orange-50" : ""}`}
    >
      {featured && (
        <div className="bg-gradient-to-r from-amber-400 to-orange-400 text-white px-4 py-2 text-sm font-medium flex items-center gap-2">
          <Crown className="w-4 h-4" />
          {t("featuredStoryOfTheDay")}
        </div>
      )}
      <CardHeader>
        <div className="flex justify-between items-start">
          <div className="space-y-2">
            <CardTitle className={`${featured ? "text-2xl" : "text-xl"} text-orange-900`}>{story.title}</CardTitle>
            <div className="flex items-center gap-4 text-sm text-orange-600">
              <div className="flex items-center gap-1">
                <User className="w-4 h-4" />
                {story.author}
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                {new Date(story.date).toLocaleDateString()}
              </div>
              <div className="flex items-center gap-1">
                <Globe className="w-4 h-4" />
                {story.language}
              </div>
            </div>
          </div>
          <Badge variant="secondary" className="bg-orange-100 text-orange-800">
            {story.category}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-gray-700 leading-relaxed">{story.content}</p>
        <div className="flex items-center justify-between pt-4 border-t border-orange-100">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleLike(story.id)}
              className={`${likedStories.has(story.id) ? "text-red-600" : "text-gray-600 hover:text-red-600"}`}
            >
              <Heart className={`w-4 h-4 mr-1 ${likedStories.has(story.id) ? "fill-current" : ""}`} />
              {story.likes + (likedStories.has(story.id) ? 1 : 0)}
            </Button>
          </div>
          <Button variant="ghost" size="sm" className="text-orange-600 hover:text-orange-700 hover:bg-orange-50">
            <Share2 className="w-4 h-4 mr-1" />
            {t("share")} ({story.shares})
          </Button>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-orange-900 mb-2">{t("communityStories")}</h1>
          <p className="text-orange-700 text-lg">{t("communitySubtitle")}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Featured Story */}
            <StoryCard story={featuredStory} featured={true} />

            {/* Tabs for different views */}
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-3 bg-orange-100">
                <TabsTrigger
                  value="latest"
                  className="data-[state=active]:bg-orange-500 data-[state=active]:text-white"
                >
                  {t("latest")}
                </TabsTrigger>
                <TabsTrigger
                  value="trending"
                  className="data-[state=active]:bg-orange-500 data-[state=active]:text-white"
                >
                  {t("trending")}
                </TabsTrigger>
                <TabsTrigger
                  value="featured"
                  className="data-[state=active]:bg-orange-500 data-[state=active]:text-white"
                >
                  {t("featured")}
                </TabsTrigger>
              </TabsList>

              <TabsContent value="latest" className="space-y-4 mt-6">
                {communityStories.map((story) => (
                  <StoryCard key={story.id} story={story} />
                ))}
              </TabsContent>

              <TabsContent value="trending" className="space-y-4 mt-6">
                {communityStories
                  .sort((a, b) => b.likes - a.likes)
                  .map((story) => (
                    <StoryCard key={story.id} story={story} />
                  ))}
              </TabsContent>

              <TabsContent value="featured" className="space-y-4 mt-6">
                <StoryCard story={featuredStory} />
                {communityStories
                  .filter((story) => story.likes > 150)
                  .map((story) => (
                    <StoryCard key={story.id} story={story} />
                  ))}
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Leaderboard */}
            <Card className="border-orange-200">
              <CardHeader>
                <CardTitle className="text-orange-900 flex items-center gap-2">
                  <Trophy className="w-5 h-5 text-amber-500" />
                  {t("topContributorsTitle")}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {leaderboard.map((user, index) => (
                  <div
                    key={user.name}
                    className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-orange-50 to-amber-50"
                  >
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                        index === 0 ? "bg-amber-500" : index === 1 ? "bg-gray-400" : "bg-orange-400"
                      }`}
                    >
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-orange-900">{user.name}</div>
                      <div className="text-sm text-orange-600">
                        {user.stories} {t("stories")} • {user.likes} {t("likes")}
                      </div>
                      <Badge variant="outline" className="text-xs mt-1 border-orange-300 text-orange-700">
                        {user.badge}
                      </Badge>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Badges Section */}
            <Card className="border-orange-200">
              <CardHeader>
                <CardTitle className="text-orange-900 flex items-center gap-2">
                  <Award className="w-5 h-5 text-amber-500" />
                  {t("culturalBadges")}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {badges.map((badge, index) => (
                  <div
                    key={index}
                    className={`flex items-center gap-3 p-3 rounded-lg ${
                      badge.earned
                        ? "bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200"
                        : "bg-gray-50 border border-gray-200"
                    }`}
                  >
                    <div className="text-2xl">{badge.icon}</div>
                    <div className="flex-1">
                      <div className={`font-medium ${badge.earned ? "text-green-800" : "text-gray-600"}`}>
                        {badge.name === "First Story"
                          ? t("firstStory")
                          : badge.name === "Wisdom Keeper"
                            ? t("wisdomKeeper")
                            : badge.name === "Cultural Ambassador"
                              ? t("culturalAmbassador")
                              : badge.name === "Story Weaver"
                                ? t("storyWeaver")
                                : badge.name === "Community Favorite"
                                  ? t("communityFavorite")
                                  : badge.name === "Voice of Heritage"
                                    ? t("voiceOfHeritage")
                                    : badge.name}
                      </div>
                      <div className={`text-sm ${badge.earned ? "text-green-600" : "text-gray-500"}`}>
                        {badge.name === "First Story"
                          ? t("firstStoryDesc")
                          : badge.name === "Wisdom Keeper"
                            ? t("wisdomKeeperDesc")
                            : badge.name === "Cultural Ambassador"
                              ? t("culturalAmbassadorDesc")
                              : badge.name === "Story Weaver"
                                ? t("storyWeaverDesc")
                                : badge.name === "Community Favorite"
                                  ? t("communityFavoriteDesc")
                                  : badge.name === "Voice of Heritage"
                                    ? t("voiceOfHeritageDesc")
                                    : badge.description}
                      </div>
                    </div>
                    {badge.earned && <Star className="w-4 h-4 text-green-500 fill-current" />}
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Floating Action Button */}
        <Link href="/share-story">
          <Button
            size="lg"
            className="fixed bottom-6 right-6 rounded-full w-14 h-14 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 shadow-lg hover:shadow-xl transition-all duration-200 z-50"
          >
            <Plus className="w-6 h-6" />
          </Button>
        </Link>
      </div>
    </div>
  )
}
