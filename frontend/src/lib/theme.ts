/** Follows the device's light/dark setting and updates live when it changes.
 *  (A manual toggle can be added later in Settings.) */
export function followSystemTheme() {
  const query = window.matchMedia('(prefers-color-scheme: dark)')
  const apply = () => document.documentElement.classList.toggle('dark', query.matches)
  apply()
  query.addEventListener('change', apply)
}
