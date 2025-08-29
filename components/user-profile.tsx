"use client"

import { useState, useEffect } from "react"
import { createClient } from "@/lib/supabase/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import {
  Trophy,
  Star,
  Heart,
  BookOpen,
  Calendar,
  Award,
  Target,
  Flame,
  Settings,
  Edit,
  LogOut,
  User,
} from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { useLanguage } from "@/lib/language-context"
import Link from "next/link"

interface UserStats {
  stories_count: number
  total_likes: number
  current_streak: number
  longest_streak: number
  languages_used: number
  categories_covered: number
}

interface UserBadge {
  id: string
  earned_at: string
  badges: {
    name: string
    description: string
    icon: string
    color: string
    requirement: number
  }
}

interface Profile {
  display_name: string
  native_language: string
  created_at: string
  bio: string
}

export function UserProfile() {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [stats, setStats] = useState<UserStats | null>(null)
  const [badges, setBadges] = useState<UserBadge[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [editedProfile, setEditedProfile] = useState({ display_name: "", bio: "" })
  const [user, setUser] = useState<any>(null)
  const { toast } = useToast()
  const { t } = useLanguage()

  const supabase = createClient()

  useEffect(() => {
    loadUserData()
  }, [])

  const loadUserData = async () => {
    try {
      const {
        data: { user: authUser },
        error: userError,
      } = await supabase.auth.getUser()

      if (userError || !authUser) {
        setIsLoading(false)
        return
      }

      setUser(authUser)

      // Load profile
      const { data: profileData } = await supabase.from("profiles").select("*").eq("id", authUser.id).single()

      if (profileData) setProfile(profileData)

      // Load user stats
      const { data: storiesData } = await supabase
        .from("stories")
        .select(`
          id,
          created_at,
          like_count,
          language_id,
          category_id
        `)
        .eq("user_id", authUser.id)

      if (storiesData) {
        const totalLikes = storiesData.reduce((sum, story) => sum + (story.like_count || 0), 0)
        const uniqueLanguages = new Set(storiesData.map((s) => s.language_id).filter(Boolean)).size
        const uniqueCategories = new Set(storiesData.map((s) => s.category_id).filter(Boolean)).size

        // Calculate streak (simplified - based on consecutive days with submissions)
        const sortedDates = storiesData
          .map((s) => new Date(s.created_at).toDateString())
          .sort()
          .filter((date, index, arr) => arr.indexOf(date) === index)

        let currentStreak = 0
        let longestStreak = 0
        let tempStreak = 1

        for (let i = 1; i < sortedDates.length; i++) {
          const prevDate = new Date(sortedDates[i - 1])
          const currDate = new Date(sortedDates[i])
          const diffTime = currDate.getTime() - prevDate.getTime()
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

          if (diffDays === 1) {
            tempStreak++
          } else {
            longestStreak = Math.max(longestStreak, tempStreak)
            tempStreak = 1
          }
        }
        longestStreak = Math.max(longestStreak, tempStreak)

        // Check if current streak is active (last submission within 2 days)
        if (sortedDates.length > 0) {
          const lastSubmission = new Date(sortedDates[sortedDates.length - 1])
          const today = new Date()
          const daysSinceLastSubmission = Math.ceil(
            (today.getTime() - lastSubmission.getTime()) / (1000 * 60 * 60 * 24),
          )
          currentStreak = daysSinceLastSubmission <= 2 ? tempStreak : 0
        }

        setStats({
          stories_count: storiesData.length,
          total_likes: totalLikes,
          current_streak: currentStreak,
          longest_streak: longestStreak,
          languages_used: uniqueLanguages,
          categories_covered: uniqueCategories,
        })

        // Check and award badges
        await checkAndAwardBadges(authUser.id, {
          stories_count: storiesData.length,
          total_likes: totalLikes,
          current_streak: currentStreak,
          longest_streak: longestStreak,
          languages_used: uniqueLanguages,
          categories_covered: uniqueCategories,
        })
      }

      // Load user badges
      const { data: badgesData } = await supabase
        .from("user_badges")
        .select(`
          id,
          earned_at,
          badges (
            name,
            description,
            icon,
            color,
            requirement
          )
        `)
        .eq("user_id", authUser.id)
        .order("earned_at", { ascending: false })

      if (badgesData) setBadges(badgesData)
    } catch (error) {
      console.error("Error loading user data:", error)
      toast({
        title: "Loading Error",
        description: "Could not load profile data.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const checkAndAwardBadges = async (userId: string, userStats: UserStats) => {
    try {
      // Get all available badges
      const { data: allBadges } = await supabase.from("badges").select("*")
      if (!allBadges) return

      // Get user's current badges
      const { data: currentBadges } = await supabase.from("user_badges").select("badge_id").eq("user_id", userId)

      const currentBadgeIds = new Set(currentBadges?.map((b) => b.badge_id) || [])

      // Check which badges should be awarded
      const badgesToAward = allBadges.filter((badge) => {
        if (currentBadgeIds.has(badge.id)) return false

        switch (badge.name) {
          case "First Story":
            return userStats.stories_count >= 1
          case "Storyteller":
            return userStats.stories_count >= 5
          case "Master Narrator":
            return userStats.stories_count >= 20
          case "Community Favorite":
            return userStats.total_likes >= 10
          case "Beloved Storyteller":
            return userStats.total_likes >= 50
          case "Streak Starter":
            return userStats.longest_streak >= 3
          case "Dedicated Contributor":
            return userStats.longest_streak >= 7
          case "Multilingual":
            return userStats.languages_used >= 2
          case "Cultural Explorer":
            return userStats.categories_covered >= 5
          default:
            return false
        }
      })

      // Award new badges
      if (badgesToAward.length > 0) {
        const badgeInserts = badgesToAward.map((badge) => ({
          user_id: userId,
          badge_id: badge.id,
        }))

        await supabase.from("user_badges").insert(badgeInserts)

        // Show toast for new badges
        badgesToAward.forEach((badge) => {
          toast({
            title: "New Badge Earned!",
            description: `You've earned the "${badge.name}" badge!`,
          })
        })
      }
    } catch (error) {
      console.error("Error checking badges:", error)
    }
  }

  const getIconComponent = (iconName: string) => {
    const icons: { [key: string]: any } = {
      trophy: Trophy,
      star: Star,
      heart: Heart,
      book: BookOpen,
      calendar: Calendar,
      award: Award,
      target: Target,
      flame: Flame,
      settings: Settings,
      edit: Edit,
      logout: LogOut,
      user: User,
    }
    const IconComponent = icons[iconName] || Award
    return <IconComponent className="w-6 h-6" />
  }

  const getNextBadgeProgress = () => {
    if (!stats) return null

    const nextMilestones = [
      { name: "Storyteller", requirement: 5, current: stats.stories_count, type: "stories" },
      { name: "Master Narrator", requirement: 20, current: stats.stories_count, type: "stories" },
      { name: "Community Favorite", requirement: 10, current: stats.total_likes, type: "likes" },
      { name: "Beloved Storyteller", requirement: 50, current: stats.total_likes, type: "likes" },
      { name: "Dedicated Contributor", requirement: 7, current: stats.longest_streak, type: "streak" },
    ]

    const nextBadge = nextMilestones.find((milestone) => milestone.current < milestone.requirement)
    if (!nextBadge) return null

    const progress = (nextBadge.current / nextBadge.requirement) * 100

    return (
      <Card className="border-purple-200">
        <CardHeader>
          <CardTitle className="text-purple-900 flex items-center gap-2">
            <Target className="w-5 h-5" />
            Next Badge Progress
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-medium text-purple-800">{nextBadge.name}</span>
              <span className="text-sm text-purple-600">
                {nextBadge.current}/{nextBadge.requirement}
              </span>
            </div>
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-purple-600">
              {nextBadge.requirement - nextBadge.current} more {nextBadge.type} needed
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    window.location.href = "/"
  }

  const handleEditProfile = () => {
    setEditedProfile({
      display_name: profile?.display_name || "",
      bio: profile?.bio || "",
    })
    setIsEditing(true)
  }

  const handleSaveProfile = async () => {
    if (!user) return

    try {
      const { error } = await supabase
        .from("profiles")
        .update({
          display_name: editedProfile.display_name,
          bio: editedProfile.bio,
        })
        .eq("id", user.id)

      if (error) throw error

      setProfile((prev) => (prev ? { ...prev, ...editedProfile } : null))
      setIsEditing(false)
      toast({
        title: t("profileUpdated"),
        description: t("profileUpdated"),
      })
    } catch (error) {
      console.error("Error updating profile:", error)
      toast({
        title: t("errorUpdatingProfile"),
        description: t("errorUpdatingProfile"),
        variant: "destructive",
      })
    }
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-orange-600">{t("loadingProfile")}</div>
      </div>
    )
  }

  if (!profile || !user) {
    return (
      <div className="text-center py-12 space-y-4">
        <User className="w-16 h-16 text-orange-400 mx-auto" />
        <p className="text-orange-600 text-lg">{t("pleaseSignIn")}</p>
        <div className="flex gap-4 justify-center">
          <Link href="/auth/login">
            <Button className="bg-orange-600 hover:bg-orange-700">{t("signInToProfile")}</Button>
          </Link>
          <Link href="/auth/sign-up">
            <Button variant="outline" className="border-orange-600 text-orange-600 hover:bg-orange-50 bg-transparent">
              {t("signUpToProfile")}
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <Card className="border-orange-200">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <Avatar className="w-16 h-16">
                <AvatarFallback className="bg-orange-100 text-orange-800 text-xl">
                  {profile.display_name.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                {isEditing ? (
                  <div className="space-y-2">
                    <Input
                      value={editedProfile.display_name}
                      onChange={(e) => setEditedProfile((prev) => ({ ...prev, display_name: e.target.value }))}
                      placeholder={t("displayName")}
                      className="text-xl font-semibold"
                    />
                  </div>
                ) : (
                  <CardTitle className="text-2xl text-orange-900">{profile.display_name}</CardTitle>
                )}
                <p className="text-orange-600">{user.email}</p>
                <p className="text-orange-600">
                  {t("nativeLanguage")}: {profile.native_language}
                </p>
                <p className="text-sm text-orange-500">
                  {t("memberSince")} {new Date(profile.created_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              {isEditing ? (
                <>
                  <Button onClick={handleSaveProfile} size="sm" className="bg-green-600 hover:bg-green-700">
                    {t("saveProfile")}
                  </Button>
                  <Button onClick={() => setIsEditing(false)} variant="outline" size="sm">
                    {t("cancel")}
                  </Button>
                </>
              ) : (
                <>
                  <Button onClick={handleEditProfile} variant="outline" size="sm">
                    <Edit className="w-4 h-4 mr-2" />
                    {t("editProfile")}
                  </Button>
                  <Button
                    onClick={handleSignOut}
                    variant="outline"
                    size="sm"
                    className="text-red-600 border-red-600 hover:bg-red-50 bg-transparent"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    {t("logout")}
                  </Button>
                </>
              )}
            </div>
          </div>
        </CardHeader>
        {/* Bio Section */}
        <CardContent>
          <div className="space-y-2">
            <h3 className="font-medium text-orange-900">{t("aboutMe")}</h3>
            {isEditing ? (
              <Textarea
                value={editedProfile.bio}
                onChange={(e) => setEditedProfile((prev) => ({ ...prev, bio: e.target.value }))}
                placeholder={t("bioPlaceholder")}
                className="min-h-[100px]"
              />
            ) : (
              <p className="text-orange-700">{profile.bio || t("bioPlaceholder")}</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="border-blue-200">
            <CardContent className="p-4 text-center">
              <BookOpen className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-800">{stats.stories_count}</div>
              <div className="text-sm text-blue-600">{t("storiesShared")}</div>
            </CardContent>
          </Card>

          <Card className="border-red-200">
            <CardContent className="p-4 text-center">
              <Heart className="w-8 h-8 text-red-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-red-800">{stats.total_likes}</div>
              <div className="text-sm text-red-600">{t("totalLikes")}</div>
            </CardContent>
          </Card>

          <Card className="border-green-200">
            <CardContent className="p-4 text-center">
              <Flame className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-green-800">{stats.current_streak}</div>
              <div className="text-sm text-green-600">{t("currentStreak")}</div>
            </CardContent>
          </Card>

          <Card className="border-purple-200">
            <CardContent className="p-4 text-center">
              <Trophy className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-purple-800">{badges.length}</div>
              <div className="text-sm text-purple-600">{t("badgesEarned")}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Next Badge Progress */}
      {getNextBadgeProgress()}

      {/* Badges Section */}
      <Card className="border-orange-200">
        <CardHeader>
          <CardTitle className="text-orange-900 flex items-center gap-2">
            <Award className="w-5 h-5" />
            {t("yourBadges")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {badges.length === 0 ? (
            <p className="text-orange-600 text-center py-8">{t("noBadgesYet")}</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {badges.map((userBadge) => (
                <div
                  key={userBadge.id}
                  className="flex items-center gap-3 p-4 rounded-lg border"
                  style={{ borderColor: userBadge.badges.color + "40" }}
                >
                  <div className="p-2 rounded-full" style={{ backgroundColor: userBadge.badges.color + "20" }}>
                    <div style={{ color: userBadge.badges.color }}>{getIconComponent(userBadge.badges.icon)}</div>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{userBadge.badges.name}</h3>
                    <p className="text-sm text-gray-600">{userBadge.badges.description}</p>
                    <p className="text-xs text-gray-500">
                      {t("earned")} {new Date(userBadge.earned_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* My Posts Section */}
      <Card className="border-orange-200">
        <CardHeader>
          <CardTitle className="text-orange-900 flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            {t("myPosts")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <BookOpen className="w-16 h-16 text-orange-300 mx-auto mb-4" />
            <p className="text-orange-600 mb-4">{t("noPostsYet")}</p>
            <Link href="/share-story">
              <Button className="bg-orange-600 hover:bg-orange-700">{t("shareFirstStory")}</Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Additional Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-indigo-200">
            <CardHeader>
              <CardTitle className="text-indigo-900">{t("culturalImpact")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-indigo-700">{t("languagesUsed")}:</span>
                <span className="font-medium text-indigo-800">{stats.languages_used}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-indigo-700">{t("categoriesCovered")}:</span>
                <span className="font-medium text-indigo-800">{stats.categories_covered}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-indigo-700">{t("longestStreak")}:</span>
                <span className="font-medium text-indigo-800">
                  {stats.longest_streak} {t("days")}
                </span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-teal-200">
            <CardHeader>
              <CardTitle className="text-teal-900">{t("communityEngagement")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between">
                <span className="text-teal-700">{t("averageLikesPerStory")}:</span>
                <span className="font-medium text-teal-800">
                  {stats.stories_count > 0 ? (stats.total_likes / stats.stories_count).toFixed(1) : "0"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-teal-700">{t("storiesThisMonth")}:</span>
                <span className="font-medium text-teal-800">-</span>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
