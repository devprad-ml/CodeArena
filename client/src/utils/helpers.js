import { FIGHTER_RANKS, SENTINEL_RANKS, PATHS } from './constants'

export function getRankForPoints(points, path) {
  const ranks = path === PATHS.FIGHTER ? FIGHTER_RANKS : SENTINEL_RANKS
  let current = ranks[0]
  for (const rank of ranks) {
    if (points >= rank.points) current = rank
    else break
  }
  return current
}

export function getNextRank(points, path) {
  const ranks = path === PATHS.FIGHTER ? FIGHTER_RANKS : SENTINEL_RANKS
  for (let i = 0; i < ranks.length - 1; i++) {
    if (points >= ranks[i].points && points < ranks[i + 1].points) {
      return ranks[i + 1]
    }
  }
  return null // at max rank
}

export function getProgressPercent(points, path) {
  const ranks = path === PATHS.FIGHTER ? FIGHTER_RANKS : SENTINEL_RANKS
  for (let i = 0; i < ranks.length - 1; i++) {
    if (points >= ranks[i].points && points < ranks[i + 1].points) {
      const range = ranks[i + 1].points - ranks[i].points
      const earned = points - ranks[i].points
      return Math.round((earned / range) * 100)
    }
  }
  return 100
}

export function formatPoints(points) {
  return points >= 1000 ? `${(points / 1000).toFixed(1)}k` : String(points)
}

export function formatDuration(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}
