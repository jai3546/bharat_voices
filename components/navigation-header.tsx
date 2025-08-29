"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/auth-context"
import { useLanguage } from "@/lib/language-context"
import { LogOut, Home, Users, UserCircle, PenTool, Compass, Globe, ChevronDown } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

const languages = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "hi", name: "हिंदी", flag: "🇮🇳" },
  { code: "ta", name: "தமிழ்", flag: "🇮🇳" },
  { code: "te", name: "తెలుగు", flag: "🇮🇳" },
]

export function NavigationHeader() {
  const pathname = usePathname()
  const { user, signOut } = useAuth()
  const { currentLanguage, setLanguage, t } = useLanguage()

  const handleSignOut = async () => {
    await signOut()
  }

  const handleLanguageChange = (languageCode: string) => {
    setLanguage(languageCode as any)
  }

  const currentLang = languages.find((lang) => lang.code === currentLanguage) || languages[0]

  return (
    <header className="bg-white border-b border-orange-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <h1 className="text-2xl font-bold text-orange-900">Bharat Voices</h1>
          </Link>

          <nav className="flex items-center space-x-4">
            <Link href="/">
              <Button
                variant={pathname === "/" ? "default" : "ghost"}
                className={
                  pathname === "/"
                    ? "bg-orange-600 hover:bg-orange-700 text-white"
                    : "text-orange-700 hover:bg-orange-50"
                }
              >
                <Home className="w-4 h-4 mr-2" />
                {t("home")}
              </Button>
            </Link>

            <Link href="/share-story">
              <Button
                variant={pathname === "/share-story" ? "default" : "ghost"}
                className={
                  pathname === "/share-story"
                    ? "bg-orange-600 hover:bg-orange-700 text-white"
                    : "text-orange-700 hover:bg-orange-50"
                }
              >
                <PenTool className="w-4 h-4 mr-2" />
                {t("shareStory")}
              </Button>
            </Link>

            <Link href="/explore">
              <Button
                variant={pathname === "/explore" ? "default" : "ghost"}
                className={
                  pathname === "/explore"
                    ? "bg-orange-600 hover:bg-orange-700 text-white"
                    : "text-orange-700 hover:bg-orange-50"
                }
              >
                <Compass className="w-4 h-4 mr-2" />
                {t("explore")}
              </Button>
            </Link>

            <Link href="/community">
              <Button
                variant={pathname === "/community" ? "default" : "ghost"}
                className={
                  pathname === "/community"
                    ? "bg-orange-600 hover:bg-orange-700 text-white"
                    : "text-orange-700 hover:bg-orange-50"
                }
              >
                <Users className="w-4 h-4 mr-2" />
                {t("community")}
              </Button>
            </Link>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-orange-700 hover:bg-orange-50 flex items-center space-x-1"
                >
                  <Globe className="w-4 h-4" />
                  <span className="hidden sm:inline">{currentLang.code.toUpperCase()}</span>
                  <ChevronDown className="w-3 h-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                {languages.map((language) => (
                  <DropdownMenuItem
                    key={language.code}
                    onClick={() => handleLanguageChange(language.code)}
                    className={`flex items-center space-x-2 cursor-pointer ${
                      currentLanguage === language.code ? "bg-orange-50 text-orange-700" : ""
                    }`}
                  >
                    <span>{language.flag}</span>
                    <span>{language.name}</span>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

            {user ? (
              <div className="flex items-center space-x-2">
                <Link href="/profile">
                  <Button
                    variant={pathname === "/profile" ? "default" : "ghost"}
                    className={
                      pathname === "/profile"
                        ? "bg-orange-600 hover:bg-orange-700 text-white"
                        : "text-orange-700 hover:bg-orange-50"
                    }
                  >
                    <UserCircle className="w-4 h-4 mr-2" />
                    {t("profile")}
                  </Button>
                </Link>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleSignOut}
                  className="border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
                >
                  <LogOut className="w-4 h-4 mr-1" />
                  {t("signOut")}
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link href="/auth/login">
                  <Button
                    variant="outline"
                    size="sm"
                    className="border-orange-300 text-orange-700 hover:bg-orange-50 bg-transparent"
                  >
                    {t("signIn")}
                  </Button>
                </Link>
                <Link href="/auth/sign-up">
                  <Button size="sm" className="bg-orange-600 hover:bg-orange-700 text-white">
                    {t("signUp")}
                  </Button>
                </Link>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
