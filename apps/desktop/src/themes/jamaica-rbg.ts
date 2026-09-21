/**
 * Jamaica RBG Theme Pack for HermesSPL Triangulum
 *
 * Red-Black-Green (Rastafarian / Pan-African) palette.
 * Two variants: dark (default) and light.
 *
 * Accent = red (#CE1126) — blood, struggle, passion
 * Surface = black (#000000) — the people, darkness before dawn
 * Success = green (#009B3A) — land, hope, growth
 *
 * Typography stays Hermes's own.
 */

import type { DesktopTheme, DesktopThemeTypography } from './types'

const SYSTEM_SANS =
  '"Segoe WPC", "Segoe UI", -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, sans-serif, ' +
  '"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", emoji'

const SYSTEM_MONO = 'Menlo, Monaco, "SF Mono", "Courier Prime", monospace, ' +
  '"Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", emoji'

export const DEFAULT_TYPOGRAPHY: DesktopThemeTypography = {
  fontSans: SYSTEM_SANS,
  fontMono: SYSTEM_MONO,
  fontUrl: 'https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap'
}

/**
 * Jamaica RBG — Dark (default)
 *
 * Black surfaces, red accents, green success states.
 * Warm, bold, unmistakably Jamaican.
 */
export const jamaicaRbgDark: DesktopTheme = {
  name: 'jamaica-rbg',
  label: 'Jamaica RBG',
  description: 'Red-Black-Green Rastafarian palette — dark mode',
  palette: {
    // Surfaces (black family)
    bg: '#0A0A0A',
    bgAlt: '#1A1A1A',
    bgElevated: '#2A2A2A',
    bgOverlay: '#000000',

    // Text (off-white on dark)
    fg: '#F5F5F5',
    fgMuted: '#B0B0B0',
    fgFaint: '#707070',

    // Accent (red = blood, struggle, passion)
    accent: '#CE1126',
    accentHover: '#E61430',
    accentMuted: '#8B1A1A',

    // Success (green = land, hope, growth)
    success: '#009B3A',
    successHover: '#00B844',
    successMuted: '#1A5C2A',

    // Warning (yellow = sun, caution)
  },

  terminal: {
    foreground: '#F5F5F5',
    black: '#0A0A0A',
    red: '#CE1126',
    green: '#009B3A',
    yellow: '#FCD116',
    blue: '#3B82F6',
    magenta: '#A855F7',
    cyan: '#06B6D4',
    white: '#E5E5E5',
    brightBlack: '#3A3A3A',
    brightRed: '#E61430',
    brightGreen: '#00B844',
    brightYellow: '#FFD966',
    brightBlue: '#60A5FA',
    brightMagenta: '#C084FC',
    brightCyan: '#22D3EE',
    brightWhite: '#FFFFFF'
  },

  darkTerminal: {
    foreground: '#F5F5F5',
    black: '#0A0A0A',
    red: '#CE1126',
    green: '#009B3A',
    yellow: '#FCD116',
    blue: '#3B82F6',
    magenta: '#A855F7',
    cyan: '#06B6D4',
    white: '#E5E5E5',
    brightBlack: '#3A3A3A',
    brightRed: '#E61430',
    brightGreen: '#00B844',
    brightYellow: '#FFD966',
    brightBlue: '#60A5FA',
    brightMagenta: '#C084FC',
    brightCyan: '#22D3EE',
    brightWhite: '#FFFFFF'
  },

  typography: DEFAULT_TYPOGRAPHY
}

/**
 * Jamaica RBG — Light
 *
 * White surfaces, deep red accents, deep green success.
 * Cleaner for daylight while keeping the identity.
 */
export const jamaicaRbgLight: DesktopTheme = {
  name: 'jamaica-rbg-light',
  label: 'Jamaica RBG Light',
  description: 'Red-Black-Green Rastafarian palette — light mode',
  palette: {
    // Surfaces (white family)
    bg: '#FFFFFF',
    bgAlt: '#F5F5F5',
    bgElevated: '#EBEBEB',
    bgOverlay: '#FFFFFF',

    // Text (dark on light)
    fg: '#0A0A0A',
    fgMuted: '#4A4A4A',
    fgFaint: '#8A8A8A',

    // Accent (deep red)
    accent: '#A00E1E',
    accentHover: '#8B0B19',
    accentMuted: '#D4A0A0',

    // Success (deep green)
    success: '#007A2E',
    successHover: '#006627',
    successMuted: '#A0C4A8',

    // Warning (amber)
  },

  terminal: {
    foreground: '#0A0A0A',
    black: '#0A0A0A',
    red: '#A00E1E',
    green: '#007A2E',
    yellow: '#B8860B',
    blue: '#1E40AF',
    magenta: '#7C3AED',
    cyan: '#0891B2',
    white: '#E5E5E5',
    brightBlack: '#3A3A3A',
    brightRed: '#CE1126',
    brightGreen: '#009B3A',
    brightYellow: '#DAA520',
    brightBlue: '#2563EB',
    brightMagenta: '#9333EA',
    brightCyan: '#0E7490',
    brightWhite: '#FFFFFF'
  },

  darkTerminal: {
    foreground: '#0A0A0A',
    black: '#0A0A0A',
    red: '#A00E1E',
    green: '#007A2E',
    yellow: '#B8860B',
    blue: '#1E40AF',
    magenta: '#7C3AED',
    cyan: '#0891B2',
    white: '#E5E5E5',
    brightBlack: '#3A3A3A',
    brightRed: '#CE1126',
    brightGreen: '#009B3A',
    brightYellow: '#DAA520',
    brightBlue: '#2563EB',
    brightMagenta: '#9333EA',
    brightCyan: '#0E7490',
    brightWhite: '#FFFFFF'
  },

  typography: DEFAULT_TYPOGRAPHY
}

export const jamaicaThemes: DesktopTheme[] = [jamaicaRbgDark, jamaicaRbgLight]
