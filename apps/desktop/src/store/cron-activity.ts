import { atom, computed } from 'nanostores'

import { Codecs, persistentAtom } from '@/lib/persisted'

/** Last time the user viewed the activity feed — drives the unread badge. */
export const $cronActivityLastViewedAt = persistentAtom<null | string>(
  'hermes.desktop.cron.activity.lastViewedAt.v1',
  null,
  Codecs.nullableText
)

/** Mark the activity feed as viewed now (clears the unread badge). */
export function markCronActivityViewed(): void {
  $cronActivityLastViewedAt.set(new Date().toISOString())
}

/** In-memory counter bump on every cron.changed event — read by the badge. */
export const $cronActivityUnreadTick = atom(0)

/** Compute unread count since last viewed (client-side estimate). */
export const $cronActivityUnreadCount = computed(
  [$cronActivityUnreadTick],
  () => $cronActivityUnreadTick.get()
)
