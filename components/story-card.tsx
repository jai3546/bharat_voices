"use client"

import { forwardRef } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface StoryCardProps {
  story: {
    title: string
    content: string
    content_type: string
    created_at: string
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
  showTranslation?: boolean
  translatedContent?: string
}

export const StoryCard = forwardRef<HTMLDivElement, StoryCardProps>(
  ({ story, showTranslation = false, translatedContent }, ref) => {
    const formatContentType = (type: string) => {
      return type.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())
    }

    return (
      <div ref={ref} className="w-[600px] bg-gradient-to-br from-orange-50 to-amber-50 p-8">
        <Card className="border-orange-200 shadow-lg">
          <CardContent className="p-8 space-y-6">
            {/* Header */}
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold text-orange-900">{story.title}</h1>
              <div className="flex justify-center gap-2">
                <Badge variant="secondary" className="bg-orange-100 text-orange-800">
                  {formatContentType(story.content_type)}
                </Badge>
                {story.categories && (
                  <Badge variant="secondary" className="text-white" style={{ backgroundColor: story.categories.color }}>
                    {story.categories.name}
                  </Badge>
                )}
              </div>
            </div>

            {/* Content */}
            <div className="space-y-4">
              <div className="bg-white rounded-lg p-6 border border-orange-100">
                <p className="text-gray-800 text-lg leading-relaxed whitespace-pre-wrap">{story.content}</p>
              </div>

              {showTranslation && translatedContent && (
                <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
                  <h4 className="text-sm font-medium text-blue-900 mb-2">English Translation</h4>
                  <p className="text-blue-800 leading-relaxed whitespace-pre-wrap">{translatedContent}</p>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="flex justify-between items-center pt-4 border-t border-orange-200">
              <div className="text-sm text-orange-600">
                <p className="font-medium">{story.profiles?.display_name || "Anonymous"}</p>
                <p>{story.languages?.name}</p>
              </div>
              <div className="text-right text-sm text-orange-500">
                <p>{new Date(story.created_at).toLocaleDateString()}</p>
                <p className="font-bold text-orange-700">Bharat Voices</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  },
)

StoryCard.displayName = "StoryCard"
