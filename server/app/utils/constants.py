PIRATE_RANKS = [
    {
        "name": "Rookie",
        "bounty": "₿0",
        "min_points": 0,
        "icon": "🏴‍☠️",
        "color": "#4a5568",
        "quote": "Every pirate starts somewhere. Set sail!",
    },
    {
        "name": "Super Rookie",
        "bounty": "₿100M",
        "min_points": 100,
        "icon": "⚔️",
        "color": "#2d3748",
        "quote": "You're making waves across the Grand Line!",
    },
    {
        "name": "Supernova",
        "bounty": "₿300M",
        "min_points": 200,
        "icon": "💫",
        "color": "#553c9a",
        "quote": "The Worst Generation acknowledges your strength!",
    },
    {
        "name": "Yonko Commander",
        "bounty": "₿1B",
        "min_points": 300,
        "icon": "🔥",
        "color": "#c53030",
        "quote": "You stand at the right hand of an Emperor!",
    },
    {
        "name": "Yonko",
        "bounty": "₿3B",
        "min_points": 400,
        "icon": "👑",
        "color": "#d69e2e",
        "quote": "The seas tremble at your name, Emperor!",
    },
    {
        "name": "Pirate King",
        "bounty": "₿5B",
        "min_points": 500,
        "icon": "🏴‍☠️👑",
        "color": "#744210",
        "quote": "You've conquered the Grand Line! But one more peak remains...",
    },
    {
        "name": "GOL D. ROGER",
        "bounty": "₿∞",
        "min_points": 600,
        "icon": "👒",
        "color": "#1a202c",
        "is_supreme": True,
        "quote": "My wealth and treasures? If you want it, I'll let you have it. Look for it; I left it all at that place!",
    },
]

MARINE_RANKS = [
    {
        "name": "Ensign",
        "title": "Junior Officer",
        "min_points": 0,
        "icon": "⚓",
        "color": "#2b6cb0",
        "quote": "Welcome to the Marines, soldier!",
    },
    {
        "name": "Lieutenant",
        "title": "Field Officer",
        "min_points": 100,
        "icon": "🎖️",
        "color": "#2c5282",
        "quote": "You're leading teams now. Design with purpose!",
    },
    {
        "name": "Captain",
        "title": "Ship Commander",
        "min_points": 200,
        "icon": "⚓🚢",
        "color": "#1a365d",
        "quote": "A ship is only as good as its architecture. Build well!",
    },
    {
        "name": "Rear Admiral",
        "title": "Fleet Officer",
        "min_points": 300,
        "icon": "🌟",
        "color": "#234e52",
        "quote": "Strategic thinking is your weapon now!",
    },
    {
        "name": "Vice Admiral",
        "title": "HQ Elite",
        "min_points": 400,
        "icon": "⭐⭐",
        "color": "#285e61",
        "quote": "The World Government relies on your designs!",
    },
    {
        "name": "Admiral",
        "title": "World Power",
        "min_points": 500,
        "icon": "🌊",
        "color": "#1a202c",
        "quote": "You shape the system itself. Few reach this height!",
    },
    {
        "name": "Fleet Admiral",
        "title": "Supreme Commander",
        "min_points": 600,
        "icon": "⚓👑",
        "color": "#171923",
        "quote": "The entire Navy answers to your architecture!",
    },
    {
        "name": "MONKEY D. GARP",
        "title": "The Hero",
        "min_points": 700,
        "icon": "🦸",
        "color": "#000000",
        "is_supreme": True,
        "quote": "I have no intention of letting the system fail. But I'm not going to stop improving it either!",
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
    "pirate": {
        "rank_name": "GOL D. ROGER",
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
    "marine": {
        "rank_name": "MONKEY D. GARP",
        "min_points": 700,
        "min_first_try_rate": 0.75,
        "min_avg_ai_score": 0.85,
        "min_lld_solved": 10,
        "min_hld_solved": 10,
        "min_perfect_scores": 5,
    },
}

# DSA Categories for Pirate path
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

# System Design Categories for Marine path
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

# Difficulty mappings based on rank
RANK_DIFFICULTY_MAP = {
    "pirate": {
        0: ["easy"],
        1: ["easy", "medium"],
        2: ["medium"],
        3: ["medium", "hard"],
        4: ["hard"],
        5: ["hard", "expert"],
        6: ["expert"],
    },
    "marine": {
        0: ["easy"],
        1: ["easy", "medium"],
        2: ["medium"],
        3: ["medium", "hard"],
        4: ["hard"],
        5: ["hard", "expert"],
        6: ["expert"],
        7: ["expert"],
    },
}
