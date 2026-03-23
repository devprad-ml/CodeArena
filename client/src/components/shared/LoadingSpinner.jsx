export default function LoadingSpinner({ size = 'md', color = 'fighter' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' }
  const colors = {
    fighter: 'border-fighter-primary',
    sentinel: 'border-sentinel-primary',
    white: 'border-white',
  }
  return (
    <div className={`${sizes[size]} border-2 ${colors[color]} border-t-transparent rounded-full animate-spin`} />
  )
}
