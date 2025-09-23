import React from 'react'

import { Button } from '@/components/ui-shadcn/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui-shadcn/dialog'
import { Input } from '@/components/ui-shadcn/input'
import { Label } from '@/components/ui-shadcn/label'
import type { SetFormPayload } from '@/typings'

type AuthData = {
  nickname: string
  sessionid: string
  ds_user_id: string
  csrftoken: string
  mid: string
  ig_did: string
}

const INITIAL_FORM = {
  nickname: '',
  sessionid: '',
  ds_user_id: '',
  csrftoken: '',
  mid: '',
  ig_did: '',
} satisfies AuthData

const FORM_ROWS = [
  { name: 'nickname' },
  { name: 'sessionid' },
  { name: 'ds_user_id' },
  { name: 'csrftoken' },
  { name: 'mid' },
  { name: 'ig_did' },
] as const

export type Props = {
  isOpen: boolean
  onClose?: () => void
}

export function AuthModal(props: Props) {
  const [form, setForm] = React.useState(INITIAL_FORM)
  if (!props.isOpen) return null

  function handleConfirm() {
    handleClose()
  }

  function handleClose() {
    props.onClose?.()
    setForm(INITIAL_FORM)
  }

  function handleChangeFormValue(payload: SetFormPayload<AuthData>) {
    setForm((prev) => ({
      ...prev,
      [payload.key]: payload.value,
    }))
  }

  return (
    <Dialog open>
      <DialogContent onClose={handleClose} className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4">
          {FORM_ROWS.map((row) => (
            <Row
              key={row.name}
              label={row.name}
              value={form[row.name]}
              onChange={(value) =>
                handleChangeFormValue({
                  key: row.name,
                  value,
                })
              }
            />
          ))}
        </div>
        <DialogFooter>
          <Button onClick={handleClose} variant="outline">
            Cancel
          </Button>
          <Button onClick={handleConfirm}>Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

type RowProps = {
  label: string
  value: string
  onChange: (value: string) => void
}

function Row(props: RowProps) {
  return (
    <div className="grid gap-3">
      <Label htmlFor={props.label}>{props.label}</Label>
      <Input
        id={props.label}
        value={props.value}
        onChange={(event) => props.onChange(event.currentTarget.value)}
      />
    </div>
  )
}
