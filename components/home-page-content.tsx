"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useLanguage } from "@/lib/language-context"
import {
  Globe,
  RefreshCw,
  Bot,
  Puzzle,
  Trophy,
  MessageCircle,
  Smartphone,
  Mic,
  Database,
  Star,
  Heart,
  Calendar,
} from "lucide-react"

export function HomePageContent() {
  const { t } = useLanguage()

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-red-50">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-orange-900 mb-6">{t("heroTitle")}</h1>
          <p className="text-xl text-orange-700 mb-8 max-w-2xl mx-auto">{t("heroSubtitle")}</p>
          <Link href="/share-story">
            <Button size="lg" className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 text-lg">
              {t("startSharing")}
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-orange-900 mb-4">{t("platformCapabilities")}</h2>
          <p className="text-lg text-orange-700">{t("platformSubtitle")}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Globe className="w-6 h-6 mr-2 text-orange-600" />
                {t("multilingualInput")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("multilingualInputDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <RefreshCw className="w-6 h-6 mr-2 text-orange-600" />
                {t("automaticTranslation")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("automaticTranslationDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Bot className="w-6 h-6 mr-2 text-orange-600" />
                {t("aiCategorization")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("aiCategorizationDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Puzzle className="w-6 h-6 mr-2 text-orange-600" />
                {t("communityWall")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("communityWallDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Trophy className="w-6 h-6 mr-2 text-orange-600" />
                {t("gamification")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("gamificationDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <MessageCircle className="w-6 h-6 mr-2 text-orange-600" />
                {t("communityInteraction")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("communityInteractionDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Smartphone className="w-6 h-6 mr-2 text-orange-600" />
                {t("personalization")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("personalizationDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Mic className="w-6 h-6 mr-2 text-orange-600" />
                {t("accessibility")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("accessibilityDesc")}</p>
            </CardContent>
          </Card>

          <Card className="border-orange-200 hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Database className="w-6 h-6 mr-2 text-orange-600" />
                {t("corpusValue")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700">{t("corpusValueDesc")}</p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Featured Story Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-orange-900 mb-4">{t("featuredStoryTitle")}</h2>
        </div>

        <div className="max-w-2xl mx-auto">
          <Card className="border-orange-200 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <Badge className="bg-orange-100 text-orange-800">{t("folkTale")}</Badge>
                <div className="flex items-center text-orange-600">
                  <Star className="w-4 h-4 mr-1 fill-current" />
                  <span className="text-sm">{t("featured")}</span>
                </div>
              </div>
              <CardTitle className="text-orange-900">The Wise Sparrow's Lesson</CardTitle>
              <p className="text-sm text-orange-600">Hindi • {t("wisdom")}</p>
            </CardHeader>
            <CardContent>
              <p className="text-orange-700 mb-4">{t("featuredStoryContent")}</p>
              <div className="flex items-center justify-between text-sm text-orange-600">
                <div className="flex items-center">
                  <Heart className="w-4 h-4 mr-1" />
                  <span>127 {t("likes")}</span>
                </div>
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>{t("sharedBy")} Priya K.</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Leaderboard Preview */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-orange-900 mb-4">{t("topContributors")}</h2>
          <p className="text-lg text-orange-700">{t("topContributorsSubtitle")}</p>
        </div>

        <div className="max-w-md mx-auto">
          <Card className="border-orange-200 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center text-orange-900">
                <Trophy className="w-6 h-6 mr-2 text-orange-600" />
                {t("leaderboard")}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-lg">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                    1
                  </div>
                  <div>
                    <p className="font-semibold text-orange-900">Rajesh M.</p>
                    <p className="text-sm text-orange-600">47 {t("stories")}</p>
                  </div>
                </div>
                <Badge className="bg-yellow-500 text-white">{t("legend")}</Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-orange-400 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                    2
                  </div>
                  <div>
                    <p className="font-semibold text-orange-900">Anita S.</p>
                    <p className="text-sm text-orange-600">32 {t("stories")}</p>
                  </div>
                </div>
                <Badge className="bg-orange-500 text-white">{t("master")}</Badge>
              </div>

              <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-orange-300 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                    3
                  </div>
                  <div>
                    <p className="font-semibold text-orange-900">Kumar P.</p>
                    <p className="text-sm text-orange-600">28 {t("stories")}</p>
                  </div>
                </div>
                <Badge className="bg-orange-400 text-white">{t("expert")}</Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-orange-900 text-orange-100 py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Bharat Voices</h3>
              <p className="text-orange-200">{t("footerDescription")}</p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">{t("quickLinks")}</h4>
              <div className="space-y-2">
                <Link href="/share-story" className="block text-orange-200 hover:text-white transition-colors">
                  {t("shareStory")}
                </Link>
                <Link href="/community" className="block text-orange-200 hover:text-white transition-colors">
                  {t("exploreStories")}
                </Link>
                <Link href="/auth/sign-up" className="block text-orange-200 hover:text-white transition-colors">
                  {t("joinCommunity")}
                </Link>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-4">{t("connect")}</h4>
              <div className="space-y-2">
                <p className="text-orange-200">contact@bharatvoices.com</p>
                <div className="flex space-x-4 mt-4">
                  <a href="#" className="text-orange-200 hover:text-white transition-colors">
                    Twitter
                  </a>
                  <a href="#" className="text-orange-200 hover:text-white transition-colors">
                    Facebook
                  </a>
                  <a href="#" className="text-orange-200 hover:text-white transition-colors">
                    Instagram
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-orange-800 mt-8 pt-8 text-center">
            <p className="text-orange-200">{t("footerCopyright")}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
