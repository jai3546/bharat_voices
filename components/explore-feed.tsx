"use client"

import { useState, useEffect } from "react"
import { createClient } from "@/lib/supabase/client"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Search, Filter, BookOpen, Database, AlertCircle } from "lucide-react"
import { StoryCard } from "@/components/story-card"

interface Story {
  id: string
  title: string
  content: string
  content_type: string
  original_language: string
  translated_content: string | null
  category: string | null
  created_at: string
  like_count: number
  profiles: {
    full_name: string | null
    username: string | null
  }
}

export function ExploreFeed() {
  const [stories, setStories] = useState<Story[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("all")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedType, setSelectedType] = useState("all")
  const [languages, setLanguages] = useState<string[]>([])
  const [categories, setCategories] = useState<string[]>([])

  const supabase = createClient()

  useEffect(() => {
    fetchStories()
    fetchFilters()
  }, [searchTerm, selectedLanguage, selectedCategory, selectedType])

  const fetchStories = async () => {
    setLoading(true)
    setError(null)

    try {
      let query = supabase
        .from("stories")
        .select(`
          *,
          profiles (
            full_name,
            username
          )
        `)
        .order("created_at", { ascending: false })

      // Apply filters
      if (searchTerm) {
        query = query.or(
          `title.ilike.%${searchTerm}%,content.ilike.%${searchTerm}%,translated_content.ilike.%${searchTerm}%`,
        )
      }

      if (selectedLanguage !== "all") {
        query = query.eq("original_language", selectedLanguage)
      }

      if (selectedCategory !== "all") {
        query = query.eq("category", selectedCategory)
      }

      if (selectedType !== "all") {
        query = query.eq("content_type", selectedType)
      }

      const { data, error } = await query

      if (error) {
        if (
          error.message.includes("Could not find the table") ||
          error.message.includes("relation") ||
          error.message.includes("does not exist")
        ) {
          setError("database_not_setup")
        } else {
          console.error("Error fetching stories:", error)
          setError("fetch_error")
        }
      } else {
        setStories(data || [])
      }
    } catch (err) {
      console.error("Unexpected error:", err)
      setError("unexpected_error")
    }

    setLoading(false)
  }

  const fetchFilters = async () => {
    try {
      // Fetch unique languages
      const { data: languageData, error: langError } = await supabase
        .from("stories")
        .select("original_language")
        .not("original_language", "is", null)

      if (!langError && languageData) {
        const uniqueLanguages = [...new Set(languageData.map((item) => item.original_language))]
        setLanguages(uniqueLanguages)
      }

      // Fetch unique categories
      const { data: categoryData, error: catError } = await supabase
        .from("stories")
        .select("category")
        .not("category", "is", null)

      if (!catError && categoryData) {
        const uniqueCategories = [...new Set(categoryData.map((item) => item.category))]
        setCategories(uniqueCategories)
      }
    } catch (err) {
      // Silently handle filter errors since they're not critical
      console.log("Could not fetch filters - database may not be set up yet")
    }
  }

  if (error === "database_not_setup") {
    return (
      <div className="space-y-6">
        <Card className="border-amber-200 bg-amber-50">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3 text-amber-800">
              <Database className="w-8 h-8" />
              <div>
                <h3 className="font-semibold text-lg">Database Setup Required</h3>
                <p className="text-amber-700 mt-1">
                  The database tables haven't been created yet. Please run the SQL scripts to set up the database.
                </p>
              </div>
            </div>
            <div className="mt-4 p-4 bg-amber-100 rounded-lg">
              <p className="text-sm text-amber-800 font-medium mb-3">To set up the database:</p>
              <div className="space-y-2 text-sm text-amber-700">
                <p>1. Go to Project Settings in the top right</p>
                <p>2. Navigate to the Scripts section</p>
                <p>3. Run all the SQL scripts in order (001_create_profiles.sql through 008_create_triggers.sql)</p>
                <p>4. Refresh this page once the scripts are complete</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error && error !== "database_not_setup") {
    return (
      <div className="space-y-6">
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3 text-red-800">
              <AlertCircle className="w-8 h-8" />
              <div>
                <h3 className="font-semibold text-lg">Error Loading Stories</h3>
                <p className="text-red-700 mt-1">
                  There was an issue loading the stories. Please try refreshing the page.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Search and Filter Section */}
      <Card className="border-orange-200">
        <CardHeader>
          <CardTitle className="flex items-center text-orange-900">
            <Filter className="w-5 h-5 mr-2" />
            Search & Filter Stories
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-orange-400 w-4 h-4" />
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
                <SelectValue placeholder="All Languages" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Languages</SelectItem>
                {languages.map((language) => (
                  <SelectItem key={language} value={language}>
                    {language}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="border-orange-200">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category}>
                    {category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedType} onValueChange={setSelectedType}>
              <SelectTrigger className="border-orange-200">
                <SelectValue placeholder="All Types" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="proverb">Proverbs</SelectItem>
                <SelectItem value="folk_tale">Folk Tales</SelectItem>
                <SelectItem value="saying">Sayings</SelectItem>
                <SelectItem value="story">Stories</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Results Summary */}
      <div className="flex items-center justify-between">
        <p className="text-orange-700">{loading ? "Loading..." : `Found ${stories.length} stories`}</p>
        {(searchTerm || selectedLanguage !== "all" || selectedCategory !== "all" || selectedType !== "all") && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSearchTerm("")
              setSelectedLanguage("all")
              setSelectedCategory("all")
              setSelectedType("all")
            }}
            className="border-orange-300 text-orange-700 hover:bg-orange-50"
          >
            Clear Filters
          </Button>
        )}
      </div>

      {/* Stories Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-4 bg-orange-200 rounded w-3/4"></div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="h-3 bg-orange-100 rounded"></div>
                  <div className="h-3 bg-orange-100 rounded w-5/6"></div>
                  <div className="h-3 bg-orange-100 rounded w-4/6"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : stories.length === 0 ? (
        <Card className="text-center py-12">
          <CardContent>
            <BookOpen className="w-12 h-12 text-orange-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-orange-900 mb-2">No stories found</h3>
            <p className="text-orange-600">Try adjusting your search terms or filters to find more stories.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stories.map((story) => (
            <StoryCard key={story.id} story={story} />
          ))}
        </div>
      )}
    </div>
  )
}
