FIGHTER_RANKS = [
    {
        "name": "Novice",
        "rating": "0",
        "min_points": 0,
        "icon": "🥊",
        "color": "#4a5568",
        "quote": "Every fighter starts somewhere. Step into the arena!",
    },
    {
        "name": "Brawler",
        "rating": "100",
        "min_points": 100,
        "icon": "⚔️",
        "color": "#2d3748",
        "quote": "You're making a name for yourself in the arena!",
    },
    {
        "name": "Striker",
        "rating": "300",
        "min_points": 200,
        "icon": "💫",
        "color": "#553c9a",
        "quote": "Your strikes land with precision and power!",
    },
    {
        "name": "Gladiator",
        "rating": "1000",
        "min_points": 300,
        "icon": "🔥",
        "color": "#c53030",
        "quote": "The colosseum roars your name!",
    },
    {
        "name": "Champion",
        "rating": "3000",
        "min_points": 400,
        "icon": "👑",
        "color": "#d69e2e",
        "quote": "Few have ever reached this level of mastery!",
    },
    {
        "name": "Grandmaster",
        "rating": "5000",
        "min_points": 500,
        "icon": "🏆",
        "color": "#744210",
        "quote": "You've conquered the arena! But one more peak remains...",
    },
    {
        "name": "LEGEND",
        "rating": "∞",
        "min_points": 600,
        "icon": "🌟",
        "color": "#1a202c",
        "is_supreme": True,
        "quote": "Algorithms bend to your will. You are the stuff of legend.",
    },
]

SENTINEL_RANKS = [
    {
        "name": "Guardian",
        "title": "Defender",
        "min_points": 0,
        "icon": "⚙️",
        "color": "#1a365d",
        "quote": "You're building systems that stand the test of time!",
    },
    {
        "name": "Warden",
        "title": "Strategist",
        "min_points": 100,
        "icon": "🏗️",
        "color": "#234e52",
        "quote": "Strategic thinking is your greatest weapon!",
    },
    {
        "name": "Protector",
        "title": "Architect",
        "min_points": 200,
        "icon": "⭐",
        "color": "#285e61",
        "quote": "Your designs shield systems from chaos!",
    },
    {
        "name": "Sovereign",
        "title": "Master Builder",
        "min_points": 300,
        "icon": "🏛️",
        "color": "#1a202c",
        "quote": "You shape the infrastructure itself. Few reach this height!",
    },
    {
        "name": "Architect Supreme",
        "title": "Supreme Commander",
        "min_points": 400,
        "icon": "🔱",
        "color": "#171923",
        "quote": "Entire systems answer to your architecture!",
    },
    {
        "name": "ORACLE",
        "title": "The Visionary",
        "min_points": 500,
        "icon": "🔮",
        "color": "#000000",
        "is_supreme": True,
        "quote": "You see the system whole — past, present, and future. True mastery.",
    },
]

# Scoring constants
SCORING = {
    "first_correct": 25,
    "wrong_submission": -5,
    "skip_penalty": -2,
    "hint_penalty": -5,
    "points_per_rank": 100,
}

# Supreme Rank Qualification Requirements
SUPREME_RANK_REQUIREMENTS = {
    "fighter": {
        "rank_name": "LEGEND",
        "min_points": 600,
        "min_first_try_rate": 0.80,
        "min_expert_solved": 10,
        "require_all_categories": True,
        "min_streak": 7,
        "categories": [
            "arrays",
            "strings",
            "linked_lists",
            "stacks_queues",
            "trees",
            "graphs",
            "dynamic_programming",
            "recursion",
            "sorting_searching",
            "bit_manipulation",
        ],
    },
    "sentinel": {
        "rank_name": "ORACLE",
        "min_points": 500,
        "min_first_try_rate": 0.75,
        "min_avg_ai_score": 0.85,
        "min_lld_solved": 10,
        "min_hld_solved": 10,
        "min_perfect_scores": 5,
    },
}

# DSA Categories for Fighter path
DSA_CATEGORIES = [
    "arrays",
    "strings",
    "linked_lists",
    "stacks_queues",
    "trees",
    "graphs",
    "dynamic_programming",
    "recursion",
    "sorting_searching",
    "bit_manipulation",
]

# System Design Categories for Sentinel path
SYSTEM_DESIGN_CATEGORIES = {
    "lld": [
        "oop_design",
        "design_patterns",
        "class_diagrams",
        "api_design",
        "database_schema",
    ],
    "hld": [
        "system_architecture",
        "scalability",
        "load_balancing",
        "caching",
        "message_queues",
        "microservices",
    ],
}

# Achievement definitions — IDs must match AchievementBadges.jsx
ACHIEVEMENTS = [
    # Fighter
    {"id": "first_blood",   "label": "First Blood",    "desc": "Solve your first problem",          "path": "fighter"},
    {"id": "hat_trick",     "label": "Hat Trick",      "desc": "Solve 3 problems in a row",         "path": "fighter"},
    {"id": "speed_demon",   "label": "Speed Demon",    "desc": "Solve a hard problem under 10 min", "path": "fighter"},
    {"id": "perfectionist", "label": "Perfectionist",  "desc": "First-try on 10 problems",          "path": "fighter"},
    {"id": "grinder",       "label": "Grinder",        "desc": "Solve 50 problems total",           "path": "fighter"},
    {"id": "graph_master",  "label": "Graph Master",   "desc": "Complete all graph problems",       "path": "fighter"},
    {"id": "dp_wizard",     "label": "DP Wizard",      "desc": "Solve 10 DP problems",              "path": "fighter"},
    {"id": "legend_born",   "label": "Legend Born",    "desc": "Achieve LEGEND rank",               "path": "fighter"},
    # Sentinel
    {"id": "architect",     "label": "Architect",      "desc": "Complete your first system design", "path": "sentinel"},
    {"id": "load_balancer", "label": "Load Balancer",  "desc": "Score 90%+ on 5 designs",           "path": "sentinel"},
    {"id": "fault_tolerant","label": "Fault Tolerant", "desc": "Zero hint usage on 5 problems",     "path": "sentinel"},
    {"id": "scalable",      "label": "Scalable",       "desc": "Complete 10 HLD problems",          "path": "sentinel"},
    {"id": "oracle_born",   "label": "Oracle Born",    "desc": "Achieve ORACLE rank",               "path": "sentinel"},
    # General
    {"id": "streak_7",      "label": "Week Warrior",   "desc": "7-day streak",                      "path": "general"},
    {"id": "streak_30",     "label": "Month Master",   "desc": "30-day streak",                     "path": "general"},
    {"id": "dual_path",     "label": "Dual Threat",    "desc": "Earn 100 pts on both paths",        "path": "general"},
]

# Difficulty mappings based on rank
RANK_DIFFICULTY_MAP = {
    "fighter": {
        0: ["easy"],
        1: ["easy", "medium"],
        2: ["medium"],
        3: ["medium", "hard"],
        4: ["hard"],
        5: ["hard", "expert"],
        6: ["expert"],
    },
    "sentinel": {
        0: ["easy"],
        1: ["medium"],
        2: ["medium", "hard"],
        3: ["hard"],
        4: ["hard", "expert"],
        5: ["expert"],
    },
}
