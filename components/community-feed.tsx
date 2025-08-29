"use client"

import { useState, useEffect } from "react"
import { createClient } from "@/lib/supabase/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Heart, Search, Filter, Play, User, Calendar, Globe, Share2 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { ShareStoryModal } from "./share-story-modal"

interface Story {
  id: string
  title: string
  content: string
  content_type: string
  created_at: string
  like_count: number
  audio_url?: string
  translated_content?: string
  profiles: {
    display_name: string
  }
  languages: {
    name: string
    native_name: string
  }
  categories: {
    name: string
    color: string
  }
}

interface Language {
  id: string
  name: string
  native_name: string
}

interface Category {
  id: string
  name: string
  color: string
}

export function CommunityFeed() {
  const [stories, setStories] = useState<Story[]>([])
  const [filteredStories, setFilteredStories] = useState<Story[]>([])
  const [languages, setLanguages] = useState<Language[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("")
  const [selectedContentType, setSelectedContentType] = useState("")
  const [likedStories, setLikedStories] = useState<Set<string>>(new Set())
  const [isLoading, setIsLoading] = useState(true)
  const [shareModalOpen, setShareModalOpen] = useState(false)
  const [selectedStoryForShare, setSelectedStoryForShare] = useState<Story | null>(null)
  const { toast } = useToast()

  const supabase = createClient()

  useEffect(() => {
    loadData()
  }, [])

  useEffect(() => {
    filterStories()
  }, [stories, searchTerm, selectedLanguage, selectedCategory, selectedContentType])

  const loadData = async () => {
    try {
      const [storiesResult, languagesResult, categoriesResult] = await Promise.all([
        supabase
          .from("stories")
          .select(`
            *,
            profiles(display_name),
            languages(name, native_name),
            categories(name, color)
          `)
          .order("created_at", { ascending: false }),
        supabase.from("languages").select("*").order("name"),
        supabase.from("categories").select("*").order("name"),
      ])

      if (storiesResult.data) setStories(storiesResult.data)
      if (languagesResult.data) setLanguages(languagesResult.data)
      if (categoriesResult.data) setCategories(categoriesResult.data)

      // Load user's liked stories
      const {
        data: { user },
      } = await supabase.auth.getUser()
      if (user) {
        const { data: likes } = await supabase.from("likes").select("story_id").eq("user_id", user.id)

        if (likes) {
          setLikedStories(new Set(likes.map((like) => like.story_id)))
        }
      }
    } catch (error) {
      console.error("Error loading data:", error)
      toast({
        title: "Loading Error",
        description: "Could not load community stories.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const filterStories = () => {
    let filtered = stories

    if (searchTerm) {
      filtered = filtered.filter(
        (story) =>
          story.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          story.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
          (story.translated_content && story.translated_content.toLowerCase().includes(searchTerm.toLowerCase())),
      )
    }

    if (selectedLanguage) {
      filtered = filtered.filter((story) => story.language_id === selectedLanguage)
    }

    if (selectedCategory) {
      filtered = filtered.filter((story) => story.category_id === selectedCategory)
    }

    if (selectedContentType) {
      filtered = filtered.filter((story) => story.content_type === selectedContentType)
    }

    setFilteredStories(filtered)
  }

  const handleLike = async (storyId: string) => {
    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please sign in to like stories.",
        variant: "destructive",
      })
      return
    }

    try {
      const isLiked = likedStories.has(storyId)

      if (isLiked) {
        // Unlike
        await supabase.from("likes").delete().eq("user_id", user.id).eq("story_id", storyId)

        setLikedStories((prev) => {
          const newSet = new Set(prev)
          newSet.delete(storyId)
          return newSet
        })

        // Update local story count
        setStories((prev) =>
          prev.map((story) => (story.id === storyId ? { ...story, like_count: story.like_count - 1 } : story)),
        )
      } else {
        // Like
        await supabase.from("likes").insert({ user_id: user.id, story_id: storyId })

        setLikedStories((prev) => new Set([...prev, storyId]))

        // Update local story count
        setStories((prev) =>
          prev.map((story) => (story.id === storyId ? { ...story, like_count: story.like_count + 1 } : story)),
        )
      }
    } catch (error) {
      console.error("Error toggling like:", error)
      toast({
        title: "Error",
        description: "Could not update like status.",
        variant: "destructive",
      })
    }
  }

  const handleShare = (story: Story) => {
    setSelectedStoryForShare(story)
    setShareModalOpen(true)
  }

  const clearFilters = () => {
    setSearchTerm("")
    setSelectedLanguage("")
    setSelectedCategory("")
    setSelectedContentType("")
  }

  const formatContentType = (type: string) => {
    return type.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())
  }

  const truncateContent = (content: string, maxLength = 200) => {
    return content.length > maxLength ? content.substring(0, maxLength) + "..." : content
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-orange-600">Loading community stories...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <Card className="border-orange-200">
        <CardHeader>
          <CardTitle className="text-orange-900 flex items-center gap-2">
            <Filter className="w-5 h-5" />
            Search & Filter Stories
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 w-4 h-4 text-orange-400" />
            <Input
              placeholder="Search stories, titles, or content..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 border-orange-200 focus:border-orange-400"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
              <SelectTrigger className="border-orange-200">
                <SelectValue placeholder="Filter by language..." />
              </SelectTrigger>
              <SelectContent>
                {languages.map((language) => (
                  <SelectItem key={language.id} value={language.id}>
                    {language.name} {language.native_name && `(${language.native_name})`}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="border-orange-200">
                <SelectValue placeholder="Filter by category..." />
              </SelectTrigger>
              <SelectContent>
                {categories.map((category) => (
                  <SelectItem key={category.id} value={category.id}>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: category.color }} />
                      {category.name}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedContentType} onValueChange={setSelectedContentType}>
              <SelectTrigger className="border-orange-200">
                <SelectValue placeholder="Filter by type..." />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="proverb">Proverb</SelectItem>
                <SelectItem value="folk_tale">Folk Tale</SelectItem>
                <SelectItem value="saying">Saying</SelectItem>
                <SelectItem value="story">Story</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {(searchTerm || selectedLanguage || selectedCategory || selectedContentType) && (
            <Button
              variant="outline"
              onClick={clearFilters}
              className="border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
            >
              Clear Filters
            </Button>
          )}
        </CardContent>
      </Card>

      {/* Stories Feed */}
      <div className="space-y-4">
        {filteredStories.length === 0 ? (
          <Card className="border-orange-200">
            <CardContent className="py-12 text-center">
              <p className="text-orange-600">No stories found matching your criteria.</p>
              <Button
                variant="outline"
                onClick={clearFilters}
                className="mt-4 border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
              >
                Clear Filters
              </Button>
            </CardContent>
          </Card>
        ) : (
          filteredStories.map((story) => (
            <Card key={story.id} className="border-orange-200 hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="space-y-2">
                    <CardTitle className="text-xl text-orange-900">{story.title}</CardTitle>
                    <div className="flex items-center gap-4 text-sm text-orange-600">
                      <div className="flex items-center gap-1">
                        <User className="w-4 h-4" />
                        {story.profiles?.display_name || "Anonymous"}
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {new Date(story.created_at).toLocaleDateString()}
                      </div>
                      {story.languages && (
                        <div className="flex items-center gap-1">
                          <Globe className="w-4 h-4" />
                          {story.languages.name}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary" className="bg-orange-100 text-orange-800">
                      {formatContentType(story.content_type)}
                    </Badge>
                    {story.categories && (
                      <Badge
                        variant="secondary"
                        className="text-white"
                        style={{ backgroundColor: story.categories.color }}
                      >
                        {story.categories.name}
                      </Badge>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="prose prose-orange max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">{truncateContent(story.content)}</p>
                </div>

                {story.translated_content && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-blue-900 mb-2">English Translation</h4>
                    <p className="text-blue-800 text-sm whitespace-pre-wrap">
                      {truncateContent(story.translated_content)}
                    </p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-orange-100">
                  <div className="flex items-center gap-4">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleLike(story.id)}
                      className={`${
                        likedStories.has(story.id)
                          ? "text-red-600 hover:text-red-700"
                          : "text-gray-600 hover:text-red-600"
                      }`}
                    >
                      <Heart className={`w-4 h-4 mr-1 ${likedStories.has(story.id) ? "fill-current" : ""}`} />
                      {story.like_count}
                    </Button>

                    {story.audio_url && (
                      <Button variant="ghost" size="sm" className="text-green-600 hover:text-green-700">
                        <Play className="w-4 h-4 mr-1" />
                        Listen
                      </Button>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleShare(story)}
                    className="text-orange-600 hover:text-orange-700 hover:bg-orange-50"
                  >
                    <Share2 className="w-4 h-4 mr-1" />
                    Share
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Share Modal */}
      {selectedStoryForShare && (
        <ShareStoryModal
          isOpen={shareModalOpen}
          onClose={() => {
            setShareModalOpen(false)
            setSelectedStoryForShare(null)
          }}
          story={selectedStoryForShare}
        />
      )}
    </div>
  )
}
