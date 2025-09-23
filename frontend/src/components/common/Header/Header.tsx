import { AuthModal } from '@/components/modals'
import { useTheme } from '@/components/providers'
import { Button } from '@/components/ui-shadcn/button'
import { Label } from '@/components/ui-shadcn/label'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from '@/components/ui-shadcn/navigation-menu'
import { Switch } from '@/components/ui-shadcn/switch'
import React from 'react'
import { NavLink } from 'react-router'

const ITEMS = [
  {
    href: '/',
    label: 'Downloader',
  },
  {
    href: '/accounts',
    label: 'Accounts',
  },
]

export function Header() {
  const [isOpenAuthModal, setIsOpenAuthModal] = React.useState(false)
  const { setTheme, theme } = useTheme()
  const isThemeChecked = theme === 'dark'

  return (
    <div className="w-full h-[60px] min-h-[60px] flex items-center">
      <div className="w-full max-w-[1280px] m-auto flex gap-10 justify-between">
        <div className="w-full">
          <NavigationMenu viewport={false}>
            <NavigationMenuList>
              {ITEMS.map((item) => {
                return (
                  <NavigationMenuItem key={item.href + item.label}>
                    <NavigationMenuLink
                      asChild
                      className={navigationMenuTriggerStyle()}
                    >
                      <NavLink to={item.href}>{item.label}</NavLink>
                    </NavigationMenuLink>
                  </NavigationMenuItem>
                )
              })}
            </NavigationMenuList>
          </NavigationMenu>
        </div>
        <div className="flex gap-5 items-center">
          <Button onClick={() => setIsOpenAuthModal(true)}>Auth</Button>
          <div className="flex flex-col gap-2 items-center">
            <Label htmlFor="theme-mode">Theme</Label>
            <Switch
              id="theme-mode"
              checked={isThemeChecked}
              onCheckedChange={() =>
                setTheme(isThemeChecked ? 'light' : 'dark')
              }
            />
          </div>
        </div>
      </div>
      <AuthModal
        isOpen={isOpenAuthModal}
        onClose={() => setIsOpenAuthModal(false)}
      />
    </div>
  )
}
