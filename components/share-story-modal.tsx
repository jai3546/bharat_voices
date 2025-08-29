"use client"

import { useState, useRef } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { StoryCard } from "./story-card"
import { Download, Share2, Twitter, Facebook, Copy, Check } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import html2canvas from "html2canvas"

interface ShareStoryModalProps {
  isOpen: boolean
  onClose: () => void
  story: any
}

export function ShareStoryModal({ isOpen, onClose, story }: ShareStoryModalProps) {
  const [includeTranslation, setIncludeTranslation] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [copied, setCopied] = useState(false)
  const cardRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  const generateImage = async () => {
    if (!cardRef.current) return null

    setIsGenerating(true)
    try {
      const canvas = await html2canvas(cardRef.current, {
        backgroundColor: "#ffffff",
        scale: 2,
        useCORS: true,
        allowTaint: true,
      })
      return canvas
    } catch (error) {
      console.error("Error generating image:", error)
      toast({
        title: "Export Error",
        description: "Could not generate image. Please try again.",
        variant: "destructive",
      })
      return null
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadImage = async () => {
    const canvas = await generateImage()
    if (!canvas) return

    const link = document.createElement("a")
    link.download = `${story.title.replace(/[^a-z0-9]/gi, "_").toLowerCase()}_story_card.png`
    link.href = canvas.toDataURL()
    link.click()

    toast({
      title: "Downloaded!",
      description: "Story card saved to your device.",
    })
  }

  const shareToSocial = (platform: string) => {
    const text = `Check out this ${story.content_type} from Bharat Voices: "${story.title}"`
    const url = window.location.origin + `/community`

    let shareUrl = ""
    switch (platform) {
      case "twitter":
        shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`
        break
      case "facebook":
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}&quote=${encodeURIComponent(text)}`
        break
    }

    if (shareUrl) {
      window.open(shareUrl, "_blank", "width=600,height=400")
    }
  }

  const copyLink = async () => {
    const text = `"${story.title}" - A ${story.content_type} from ${story.profiles?.display_name || "Anonymous"} on Bharat Voices\n\n${story.content}\n\nDiscover more cultural stories at ${window.location.origin}`

    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
      toast({
        title: "Copied!",
        description: "Story text copied to clipboard.",
      })
    } catch (error) {
      toast({
        title: "Copy Failed",
        description: "Could not copy to clipboard.",
        variant: "destructive",
      })
    }
  }

  const shareNative = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${story.title} - Bharat Voices`,
          text: `Check out this ${story.content_type}: "${story.content.substring(0, 100)}..."`,
          url: window.location.origin + `/community`,
        })
      } catch (error) {
        console.error("Error sharing:", error)
      }
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-orange-900">Share Story</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Options */}
          <div className="flex items-center space-x-2">
            <Switch
              id="include-translation"
              checked={includeTranslation}
              onCheckedChange={setIncludeTranslation}
              disabled={!story.translated_content}
            />
            <Label htmlFor="include-translation" className="text-sm">
              Include English translation
              {!story.translated_content && " (not available)"}
            </Label>
          </div>

          {/* Preview */}
          <div className="flex justify-center bg-gray-100 p-4 rounded-lg">
            <StoryCard
              ref={cardRef}
              story={story}
              showTranslation={includeTranslation}
              translatedContent={story.translated_content}
            />
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Button
              onClick={downloadImage}
              disabled={isGenerating}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              <Download className="w-4 h-4 mr-2" />
              {isGenerating ? "Generating..." : "Download"}
            </Button>

            <Button
              onClick={copyLink}
              variant="outline"
              className="border-blue-300 text-blue-700 hover:bg-blue-50 bg-transparent"
            >
              {copied ? <Check className="w-4 h-4 mr-2" /> : <Copy className="w-4 h-4 mr-2" />}
              {copied ? "Copied!" : "Copy Text"}
            </Button>

            <Button
              onClick={() => shareToSocial("twitter")}
              variant="outline"
              className="border-sky-300 text-sky-700 hover:bg-sky-50"
            >
              <Twitter className="w-4 h-4 mr-2" />
              Twitter
            </Button>

            <Button
              onClick={() => shareToSocial("facebook")}
              variant="outline"
              className="border-blue-600 text-blue-700 hover:bg-blue-50"
            >
              <Facebook className="w-4 h-4 mr-2" />
              Facebook
            </Button>
          </div>

          {/* Native Share (if supported) */}
          {navigator.share && (
            <Button
              onClick={shareNative}
              variant="outline"
              className="w-full border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share via Device
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
