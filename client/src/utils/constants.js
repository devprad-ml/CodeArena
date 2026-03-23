// ============================================================
// CODEARENA FRONTEND CONSTANTS — single source of truth
// Mirror of server/app/utils/constants.py
// ============================================================

export const PATHS = {
  FIGHTER: 'fighter',
  SENTINEL: 'sentinel',
}

export const FIGHTER_RANKS = [
  { name: 'Novice',      points: 0,   difficulty: 'Easy',        color: '#9ca3af' },
  { name: 'Brawler',     points: 100, difficulty: 'Easy-Medium', color: '#34d399' },
  { name: 'Striker',     points: 300, difficulty: 'Medium',      color: '#60a5fa' },
  { name: 'Gladiator',   points: 600, difficulty: 'Medium-Hard', color: '#a78bfa' },
  { name: 'Champion',    points: 1000,difficulty: 'Hard',        color: '#fbbf24' },
  { name: 'Grandmaster', points: 1400,difficulty: 'Hard',        color: '#f97316' },
  { name: 'LEGEND',      points: 2000,difficulty: 'Expert',      color: '#e63946', supreme: true },
]

export const SENTINEL_RANKS = [
  { name: 'Guardian',          points: 0,   difficulty: 'Easy',        color: '#9ca3af' },
  { name: 'Warden',            points: 100, difficulty: 'Easy-Medium', color: '#34d399' },
  { name: 'Protector',         points: 300, difficulty: 'Medium',      color: '#60a5fa' },
  { name: 'Sovereign',         points: 600, difficulty: 'Medium-Hard', color: '#a78bfa' },
  { name: 'Architect Supreme', points: 1000,difficulty: 'Hard',        color: '#fbbf24' },
  { name: 'ORACLE',            points: 1400,difficulty: 'Expert',      color: '#0077b6', supreme: true },
]

export const SCORING = {
  CORRECT_FIRST_TRY: 25,
  CORRECT_AFTER_WRONG: 25,  // gross, penalty applied separately
  WRONG_SUBMISSION: -5,
  SKIP_QUESTION: -2,
  HINT_PENALTY: -3,
}

export const SUPPORTED_LANGUAGES = [
  { id: 'python',     label: 'Python 3',    judge0Id: 71, monacoLang: 'python'     },
  { id: 'javascript', label: 'JavaScript',  judge0Id: 63, monacoLang: 'javascript' },
  { id: 'java',       label: 'Java',        judge0Id: 62, monacoLang: 'java'       },
  { id: 'cpp',        label: 'C++',         judge0Id: 54, monacoLang: 'cpp'        },
  { id: 'c',          label: 'C',           judge0Id: 50, monacoLang: 'c'          },
  { id: 'go',         label: 'Go',          judge0Id: 60, monacoLang: 'go'         },
  { id: 'rust',       label: 'Rust',        judge0Id: 73, monacoLang: 'rust'       },
]

export const TIMER_OPTIONS = [15, 30, 45, 60] // minutes

export const LEGEND_REQUIREMENTS = {
  points: 600,
  first_try_rate: 0.80,
  expert_solved: 10,
  current_streak: 7,
}

export const ORACLE_REQUIREMENTS = {
  points: 500,
  first_try_rate: 0.75,
  avg_ai_score: 0.85,
  lld_completed: 10,
  hld_completed: 10,
  perfect_scores: 5,
}

export const API_BASE = '/api/v1'
