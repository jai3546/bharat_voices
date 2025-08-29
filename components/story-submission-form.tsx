"use client"

import type React from "react"

import { useState, useRef } from "react"
import { createClient } from "@/lib/supabase/client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Mic, MicOff, Play, Pause, Upload, Sparkles, Languages } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface Language {
  id: string
  name: string
  native_name: string
}

interface Category {
  id: string
  name: string
  description: string
  color: string
}

export function StorySubmissionForm() {
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [contentType, setContentType] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("")
  const [dialect, setDialect] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("")
  const [languages, setLanguages] = useState<Language[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [translatedContent, setTranslatedContent] = useState("")
  const [suggestedCategory, setSuggestedCategory] = useState("")
  const [isTranslating, setIsTranslating] = useState(false)
  const [isCategorizing, setIsCategorizing] = useState(false)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const { toast } = useToast()

  useState(() => {
    const loadData = async () => {
      const supabase = createClient()

      const [languagesResult, categoriesResult] = await Promise.all([
        supabase.from("languages").select("*").order("name"),
        supabase.from("categories").select("*").order("name"),
      ])

      if (languagesResult.data) setLanguages(languagesResult.data)
      if (categoriesResult.data) setCategories(categoriesResult.data)
    }

    loadData()
  })

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder

      const chunks: BlobPart[] = []
      mediaRecorder.ondataavailable = (event) => {
        chunks.push(event.data)
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/wav" })
        setAudioBlob(blob)
        stream.getTracks().forEach((track) => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      toast({
        title: "Recording Error",
        description: "Could not access microphone. Please check permissions.",
        variant: "destructive",
      })
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const playAudio = () => {
    if (audioBlob) {
      const audioUrl = URL.createObjectURL(audioBlob)
      audioRef.current = new Audio(audioUrl)
      audioRef.current.play()
      setIsPlaying(true)

      audioRef.current.onended = () => {
        setIsPlaying(false)
        URL.revokeObjectURL(audioUrl)
      }
    }
  }

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }

  const handleTranslate = async () => {
    if (!content || !selectedLanguage) {
      toast({
        title: "Missing Information",
        description: "Please enter content and select a language first.",
        variant: "destructive",
      })
      return
    }

    setIsTranslating(true)
    setTranslatedContent("")

    try {
      const selectedLang = languages.find((lang) => lang.id === selectedLanguage)
      const sourceLangName = selectedLang?.name || "the selected language"

      const response = await fetch("/api/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content,
          sourceLanguage: sourceLangName,
          targetLanguage: "English",
        }),
      })

      if (!response.ok) {
        throw new Error("Translation failed")
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let fullTranslation = ""

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value, { stream: true })
          fullTranslation += chunk
          setTranslatedContent(fullTranslation)
        }
      }

      toast({
        title: "Translation Complete",
        description: "Your content has been translated to English.",
      })
    } catch (error) {
      console.error("Translation error:", error)
      toast({
        title: "Translation Failed",
        description: "Could not translate content. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsTranslating(false)
    }
  }

  const handleCategorize = async () => {
    if (!content || !contentType) {
      toast({
        title: "Missing Information",
        description: "Please enter content and select content type first.",
        variant: "destructive",
      })
      return
    }

    setIsCategorizing(true)
    setSuggestedCategory("")

    try {
      const response = await fetch("/api/categorize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content,
          contentType,
        }),
      })

      if (!response.ok) {
        throw new Error("Categorization failed")
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let fullCategory = ""

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value, { stream: true })
          fullCategory += chunk
          setSuggestedCategory(fullCategory.trim())
        }
      }

      const matchingCategory = categories.find((cat) => cat.name.toLowerCase() === fullCategory.trim().toLowerCase())
      if (matchingCategory) {
        setSelectedCategory(matchingCategory.id)
      }

      toast({
        title: "Categorization Complete",
        description: "AI has suggested a category for your content.",
      })
    } catch (error) {
      console.error("Categorization error:", error)
      toast({
        title: "Categorization Failed",
        description: "Could not categorize content. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsCategorizing(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!title || !content || !contentType || !selectedLanguage) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      })
      return
    }

    setIsSubmitting(true)
    const supabase = createClient()

    try {
      const {
        data: { user },
        error: userError,
      } = await supabase.auth.getUser()

      if (userError || !user) {
        toast({
          title: "Authentication Required",
          description: "Please sign in to submit your story.",
          variant: "destructive",
        })
        return
      }

      let audioUrl = null
      if (audioBlob) {
        const fileName = `audio/${user.id}/${Date.now()}.wav`
        const { data: uploadData, error: uploadError } = await supabase.storage
          .from("audio")
          .upload(fileName, audioBlob)

        if (uploadError) {
          console.error("Audio upload error:", uploadError)
        } else {
          const {
            data: { publicUrl },
          } = supabase.storage.from("audio").getPublicUrl(fileName)
          audioUrl = publicUrl
        }
      }

      const { error: insertError } = await supabase.from("stories").insert({
        user_id: user.id,
        title,
        content,
        content_type: contentType,
        language_id: selectedLanguage || null,
        dialect: dialect || null,
        category_id: selectedCategory || null,
        audio_url: audioUrl,
        translated_content: translatedContent || null,
      })

      if (insertError) throw insertError

      toast({
        title: "Story Submitted!",
        description: "Your story has been shared with the community.",
      })

      setTitle("")
      setContent("")
      setContentType("")
      setSelectedLanguage("")
      setDialect("")
      setSelectedCategory("")
      setAudioBlob(null)
      setTranslatedContent("")
      setSuggestedCategory("")
    } catch (error) {
      console.error("Submission error:", error)
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your story. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="border-orange-200 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-orange-100 to-amber-100">
          <CardTitle className="text-2xl text-orange-900">Share Your Story</CardTitle>
          <CardDescription className="text-orange-700">
            Preserve and share your cultural wisdom with the world
          </CardDescription>
        </CardHeader>
        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="title" className="text-orange-900 font-medium">
                Title *
              </Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter a title for your story..."
                className="border-orange-200 focus:border-orange-400"
                required
              />
            </div>

            <div className="space-y-2">
              <Label className="text-orange-900 font-medium">Content Type *</Label>
              <Select value={contentType} onValueChange={setContentType} required>
                <SelectTrigger className="border-orange-200 focus:border-orange-400">
                  <SelectValue placeholder="Select content type..." />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="proverb">Proverb</SelectItem>
                  <SelectItem value="folk_tale">Folk Tale</SelectItem>
                  <SelectItem value="saying">Saying</SelectItem>
                  <SelectItem value="story">Story</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label className="text-orange-900 font-medium">Language *</Label>
              <Select value={selectedLanguage} onValueChange={setSelectedLanguage} required>
                <SelectTrigger className="border-orange-200 focus:border-orange-400">
                  <SelectValue placeholder="Select language..." />
                </SelectTrigger>
                <SelectContent>
                  {languages.map((language) => (
                    <SelectItem key={language.id} value={language.id}>
                      {language.name} {language.native_name && `(${language.native_name})`}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="dialect" className="text-orange-900 font-medium">
                Dialect (Optional)
              </Label>
              <Input
                id="dialect"
                value={dialect}
                onChange={(e) => setDialect(e.target.value)}
                placeholder="Specify dialect if applicable..."
                className="border-orange-200 focus:border-orange-400"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-orange-900 font-medium">Category</Label>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="border-orange-200 focus:border-orange-400">
                  <SelectValue placeholder="Select a category..." />
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
            </div>

            <div className="space-y-2">
              <Label htmlFor="content" className="text-orange-900 font-medium">
                Content *
              </Label>
              <Textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Share your story, proverb, or saying..."
                className="min-h-32 border-orange-200 focus:border-orange-400"
                required
              />
              <div className="flex gap-2 mt-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleTranslate}
                  disabled={isTranslating || !content || !selectedLanguage}
                  className="border-blue-300 text-blue-700 hover:bg-blue-50 bg-transparent"
                >
                  {isTranslating ? (
                    <>
                      <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                      Translating...
                    </>
                  ) : (
                    <>
                      <Languages className="w-4 h-4 mr-2" />
                      AI Translate
                    </>
                  )}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleCategorize}
                  disabled={isCategorizing || !content || !contentType}
                  className="border-purple-300 text-purple-700 hover:bg-purple-50 bg-transparent"
                >
                  {isCategorizing ? (
                    <>
                      <Sparkles className="w-4 h-4 mr-2 animate-spin" />
                      Categorizing...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 mr-2" />
                      AI Categorize
                    </>
                  )}
                </Button>
              </div>
            </div>

            {translatedContent && (
              <div className="space-y-2">
                <Label className="text-blue-900 font-medium">AI Translation (English)</Label>
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-blue-800 whitespace-pre-wrap">{translatedContent}</p>
                </div>
              </div>
            )}

            {suggestedCategory && (
              <div className="space-y-2">
                <Label className="text-purple-900 font-medium">AI Suggested Category</Label>
                <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                  {suggestedCategory}
                </Badge>
              </div>
            )}

            <div className="space-y-3">
              <Label className="text-orange-900 font-medium">Audio Recording (Optional)</Label>
              <div className="flex items-center gap-3">
                {!isRecording ? (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={startRecording}
                    className="border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
                  >
                    <Mic className="w-4 h-4 mr-2" />
                    Start Recording
                  </Button>
                ) : (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={stopRecording}
                    className="border-red-300 text-red-700 hover:bg-red-50 bg-transparent"
                  >
                    <MicOff className="w-4 h-4 mr-2" />
                    Stop Recording
                  </Button>
                )}

                {audioBlob && (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={isPlaying ? pauseAudio : playAudio}
                    className="border-green-300 text-green-700 hover:bg-green-50 bg-transparent"
                  >
                    {isPlaying ? <Pause className="w-4 h-4 mr-2" /> : <Play className="w-4 h-4 mr-2" />}
                    {isPlaying ? "Pause" : "Play"}
                  </Button>
                )}
              </div>

              {isRecording && (
                <Badge variant="secondary" className="bg-red-100 text-red-800">
                  Recording in progress...
                </Badge>
              )}

              {audioBlob && (
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  Audio recorded successfully
                </Badge>
              )}
            </div>

            <Button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white font-medium py-3"
            >
              {isSubmitting ? (
                <>
                  <Upload className="w-4 h-4 mr-2 animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4 mr-2" />
                  Share Your Story
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
