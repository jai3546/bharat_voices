"use client"

import { useState, useRef } from "react"
import { Search, Filter, BookOpen, Heart, Eye, Star, Sparkles, Mic, MicOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useLanguage } from "@/lib/language-context"

// Dummy data for story cards
const sampleStories = [
  {
    id: 1,
    title: "The Wise Elephant's Teaching",
    excerpt:
      "In the heart of Kerala, an old elephant taught villagers about patience and wisdom through his gentle actions...",
    category: "Ancient Wisdom",
    language: "Malayalam",
    author: "Priya Nair",
    likes: 127,
    views: 1240,
  },
  {
    id: 2,
    title: "The Laughing Merchant",
    excerpt:
      "A Punjabi trader's humor could turn the sourest deal into friendship, teaching us that laughter opens all doors...",
    category: "Cultural Humor",
    language: "Punjabi",
    author: "Harpreet Singh",
    likes: 89,
    views: 890,
  },
  {
    id: 3,
    title: "Rivers Remember Everything",
    excerpt:
      "The Ganges whispered ancient secrets to a young girl, revealing how nature holds the memory of all civilizations...",
    category: "Nature Stories",
    language: "Hindi",
    author: "Meera Sharma",
    likes: 203,
    views: 1560,
  },
  {
    id: 4,
    title: "The Coconut Tree's Promise",
    excerpt:
      "Every part of the coconut tree serves humanity, just as every person has a purpose in the grand design of life...",
    category: "Global Proverbs",
    language: "Tamil",
    author: "Ravi Kumar",
    likes: 156,
    views: 1100,
  },
  {
    id: 5,
    title: "The Dancing Peacock's Lesson",
    excerpt: "When the monsoon arrives, peacocks dance not for show, but to celebrate life's abundance and beauty...",
    category: "Nature Stories",
    language: "Bengali",
    author: "Anita Das",
    likes: 178,
    views: 1320,
  },
  {
    id: 6,
    title: "The Spice Seller's Wisdom",
    excerpt:
      "In the bustling markets of Old Delhi, a spice seller shared the secret ingredient that makes every dish special...",
    category: "Ancient Wisdom",
    language: "Urdu",
    author: "Ahmed Khan",
    likes: 134,
    views: 980,
  },
]

const featuredCategories = [
  {
    title: "Global Proverbs",
    description: "Timeless wisdom from every corner of the world",
    icon: "🌍",
    count: 1247,
    gradient: "from-blue-500 to-cyan-500",
  },
  {
    title: "Ancient Wisdom",
    description: "Sacred teachings passed down through generations",
    icon: "📜",
    count: 892,
    gradient: "from-purple-500 to-pink-500",
  },
  {
    title: "Cultural Humor",
    description: "Laughter that transcends all boundaries",
    icon: "😄",
    count: 634,
    gradient: "from-yellow-500 to-orange-500",
  },
  {
    title: "Nature Stories",
    description: "Tales of harmony between humans and nature",
    icon: "🌿",
    count: 756,
    gradient: "from-green-500 to-emerald-500",
  },
]

const mostViewed = [
  { title: "The Last Storyteller of Kashmir", views: 3420, author: "Rajesh Koul" },
  { title: "Grandmother's Monsoon Recipe", views: 2890, author: "Lakshmi Iyer" },
  { title: "The Fisherman's Philosophy", views: 2650, author: "Joseph D'Souza" },
]

const editorsPicks = [
  { title: "The Weaver's Dream", category: "Ancient Wisdom", author: "Sunita Devi" },
  { title: "Chai and Conversations", category: "Cultural Humor", author: "Vikram Patel" },
  { title: "The Banyan Tree's Secret", category: "Nature Stories", author: "Arjun Reddy" },
]

export function ExploreContent() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedLanguage, setSelectedLanguage] = useState("all")
  const [isListening, setIsListening] = useState(false)
  const [speechSupported, setSpeechSupported] = useState(false)
  const recognitionRef = useRef<any>(null)
  const { t } = useLanguage()

  useState(() => {
    if (typeof window !== "undefined" && ("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      setSpeechSupported(true)
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = "en-US"

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript
        setSearchQuery(transcript)
        setIsListening(false)
      }

      recognitionRef.current.onerror = () => {
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }
  })

  const toggleVoiceSearch = () => {
    if (!speechSupported) return

    if (isListening) {
      recognitionRef.current?.stop()
      setIsListening(false)
    } else {
      recognitionRef.current?.start()
      setIsListening(true)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-orange-900 mb-4">{t("exploreCulturalStories")}</h1>
        <p className="text-xl text-orange-700 max-w-3xl mx-auto leading-relaxed">{t("exploreSubtitle")}</p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 mb-12 shadow-lg border border-orange-100">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-400 h-5 w-5" />
            <Input
              placeholder={t("searchPlaceholder")}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-14 h-12 border-orange-200 focus:border-orange-400 focus:ring-orange-400"
            />
            {speechSupported && (
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={toggleVoiceSearch}
                      className={`absolute right-2 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 rounded-full transition-all duration-200 ${
                        isListening
                          ? "bg-orange-500 text-white hover:bg-orange-600 animate-pulse"
                          : "text-orange-500 hover:bg-orange-100 hover:text-orange-600"
                      }`}
                    >
                      {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>{isListening ? t("stopListening") : t("tapToSpeak")}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            )}
          </div>
          <div className="flex gap-3">
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-48 h-12 border-orange-200">
                <Filter className="h-4 w-4 mr-2 text-orange-400" />
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">{t("allCategories")}</SelectItem>
                <SelectItem value="global-proverbs">{t("globalProverbs")}</SelectItem>
                <SelectItem value="ancient-wisdom">{t("ancientWisdom")}</SelectItem>
                <SelectItem value="cultural-humor">{t("culturalHumor")}</SelectItem>
                <SelectItem value="nature-stories">{t("natureStories")}</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
              <SelectTrigger className="w-48 h-12 border-orange-200">
                <SelectValue placeholder="Language" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">{t("allLanguages")}</SelectItem>
                <SelectItem value="hindi">Hindi</SelectItem>
                <SelectItem value="bengali">Bengali</SelectItem>
                <SelectItem value="tamil">Tamil</SelectItem>
                <SelectItem value="malayalam">Malayalam</SelectItem>
                <SelectItem value="punjabi">Punjabi</SelectItem>
                <SelectItem value="urdu">Urdu</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Story Cards Grid */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-orange-900 mb-8">{t("latestStories")}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sampleStories.map((story) => (
            <Card
              key={story.id}
              className="group hover:shadow-xl transition-all duration-300 border-orange-100 hover:border-orange-300 bg-white/90 backdrop-blur-sm"
            >
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start mb-2">
                  <Badge variant="secondary" className="bg-orange-100 text-orange-800 hover:bg-orange-200">
                    {story.category}
                  </Badge>
                  <Badge variant="outline" className="border-amber-300 text-amber-700">
                    {story.language}
                  </Badge>
                </div>
                <CardTitle className="text-xl text-orange-900 group-hover:text-orange-700 transition-colors line-clamp-2">
                  {story.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-orange-700 mb-4 line-clamp-3 leading-relaxed">{story.excerpt}</p>
                <div className="flex items-center justify-between text-sm text-orange-600 mb-4">
                  <span>
                    {t("by")} {story.author}
                  </span>
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                      <Heart className="h-4 w-4" />
                      <span>{story.likes}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Eye className="h-4 w-4" />
                      <span>{story.views}</span>
                    </div>
                  </div>
                </div>
                <Button className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white">
                  <BookOpen className="h-4 w-4 mr-2" />
                  {t("readMore")}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Featured Categories */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-orange-900 mb-8">{t("featuredCategories")}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {featuredCategories.map((category, index) => (
            <Card
              key={index}
              className="group cursor-pointer hover:shadow-xl transition-all duration-300 border-orange-100 hover:border-orange-300 overflow-hidden"
            >
              <div className={`h-2 bg-gradient-to-r ${category.gradient}`}></div>
              <CardContent className="p-6 text-center">
                <div className="text-4xl mb-4">{category.icon}</div>
                <h3 className="text-xl font-bold text-orange-900 mb-2">
                  {category.title === "Global Proverbs"
                    ? t("globalProverbs")
                    : category.title === "Ancient Wisdom"
                      ? t("ancientWisdom")
                      : category.title === "Cultural Humor"
                        ? t("culturalHumor")
                        : category.title === "Nature Stories"
                          ? t("natureStories")
                          : category.title}
                </h3>
                <p className="text-orange-700 mb-4 text-sm leading-relaxed">
                  {category.title === "Global Proverbs"
                    ? t("globalProverbsDesc")
                    : category.title === "Ancient Wisdom"
                      ? t("ancientWisdomDesc")
                      : category.title === "Cultural Humor"
                        ? t("culturalHumorDesc")
                        : category.title === "Nature Stories"
                          ? t("natureStoriesDesc")
                          : category.description}
                </p>
                <div className="text-2xl font-bold text-orange-600">{category.count.toLocaleString()}</div>
                <div className="text-sm text-orange-500">{t("storiesCount")}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Highlights Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
        {/* Most Viewed */}
        <Card className="border-orange-100 bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-900">
              <Eye className="h-5 w-5 text-orange-600" />
              {t("mostViewed")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mostViewed.map((story, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 rounded-lg bg-orange-50 hover:bg-orange-100 transition-colors cursor-pointer"
                >
                  <div>
                    <div className="font-semibold text-orange-900 text-sm">{story.title}</div>
                    <div className="text-orange-600 text-xs">
                      {t("by")} {story.author}
                    </div>
                  </div>
                  <div className="text-orange-700 font-bold text-sm">{story.views.toLocaleString()}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Editor's Picks */}
        <Card className="border-orange-100 bg-white/90 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-900">
              <Star className="h-5 w-5 text-orange-600" />
              {t("editorsPicks")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {editorsPicks.map((story, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 rounded-lg bg-orange-50 hover:bg-orange-100 transition-colors cursor-pointer"
                >
                  <div>
                    <div className="font-semibold text-orange-900 text-sm">{story.title}</div>
                    <div className="text-orange-600 text-xs">
                      {t("by")} {story.author}
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-orange-200 text-orange-800 text-xs">
                    {story.category}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Coming Soon Banner */}
      <Card className="bg-gradient-to-r from-orange-500 to-amber-500 text-white border-0 mb-8">
        <CardContent className="p-8 text-center">
          <Sparkles className="h-12 w-12 mx-auto mb-4 text-white/90" />
          <h3 className="text-2xl font-bold mb-2">{t("comingSoon")}</h3>
          <p className="text-white/90 max-w-2xl mx-auto">{t("comingSoonDesc")}</p>
        </CardContent>
      </Card>
    </div>
  )
}
