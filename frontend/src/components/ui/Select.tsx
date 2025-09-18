import {
  Select as ShadcnSelect,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui-shadcn/select'

export type SelectOption = {
  value: string
  label: string
}

export type Props = {
  value: string
  placeholder?: string
  options: SelectOption[]
  onChange: (value: string) => void
}

export function Select(props: Props) {
  return (
    <ShadcnSelect onValueChange={props.onChange} value={props.value}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder={props.placeholder} />
      </SelectTrigger>
      <SelectContent>
        {props.options.map((option) => {
          return (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          )
        })}
      </SelectContent>
    </ShadcnSelect>
  )
}
