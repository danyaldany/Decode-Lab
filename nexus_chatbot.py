"""
═══════════════════════════════════════════════════════════════════════════════
    NEXUS CHATBOT — Professional Streamlit UI
    ChatGPT-Style Interface with Conversation History Sidebar
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import re
import random
import json
import os
from datetime import datetime
from collections import deque
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
import uuid
import time


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & STYLING
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & STYLING - PROFESSIONAL UI v2.0
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
<style>
    /* ============ GLOBAL STYLES ============ */
    * {
        font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* Main chat area styling */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    .main {
        background: transparent;
    }
    
    /* ============ SCROLLBAR STYLING ============ */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366F1, #8B5CF6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #8B5CF6, #A78BFA);
    }
    
    /* ============ CHAT MESSAGE CONTAINERS ============ */
    .chat-message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 0.75rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 1rem;
        animation: messageSlideIn 0.3s ease-out;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4);
        }
        50% {
            box-shadow: 0 0 0 15px rgba(99, 102, 241, 0);
        }
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-left: 20px;
        border-bottom-right-radius: 4px;
    }
    
    .chat-message.user::before {
        content: '';
        position: absolute;
        right: -10px;
        top: 20px;
        width: 0;
        height: 0;
        border-left: 10px solid rgba(99, 102, 241, 0.2);
        border-top: 6px solid transparent;
        border-bottom: 6px solid transparent;
    }
    
    .chat-message.bot {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.6));
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-right: 20px;
        border-bottom-left-radius: 4px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message.bot::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 20px;
        width: 0;
        height: 0;
        border-right: 10px solid rgba(148, 163, 184, 0.1);
        border-top: 6px solid transparent;
        border-bottom: 6px solid transparent;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* ============ AVATAR STYLING ============ */
    .avatar {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .avatar.user {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        animation: pulse 2s infinite;
    }
    
    .avatar.bot {
        background: linear-gradient(135deg, #10B981, #059669);
        animation: pulse 3s infinite;
    }
    
    /* ============ MESSAGE CONTENT ============ */
    .message-content {
        flex-grow: 1;
        color: #E2E8F0;
        font-size: 15px;
        line-height: 1.7;
        letter-spacing: 0.3px;
    }
    
    .message-content h1, .message-content h2, .message-content h3 {
        color: #F1F5F9;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .message-content strong {
        color: #A78BFA;
        font-weight: 600;
    }
    
    .message-content code {
        background: rgba(99, 102, 241, 0.1);
        padding: 2px 8px;
        border-radius: 6px;
        color: #A78BFA;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 13px;
    }
    
    .message-content ul, .message-content ol {
        margin-left: 1.5rem;
    }
    
    .message-content li {
        margin-bottom: 0.3rem;
    }
    
    .message-content a {
        color: #818CF8;
        text-decoration: none;
        border-bottom: 1px dashed #818CF8;
        transition: all 0.3s ease;
    }
    
    .message-content a:hover {
        color: #A78BFA;
        border-bottom: 1px solid #A78BFA;
    }
    
    /* ============ SIDEBAR STYLING ============ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        min-width: 280px;
        max-width: 280px;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
        background: transparent;
    }
    
    /* Sidebar header */
    .sidebar-header {
        padding: 24px 20px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05));
    }
    
    .sidebar-title {
        color: #F1F5F9;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.5px;
    }
    
    .sidebar-title span {
        background: linear-gradient(135deg, #6366F1, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar buttons */
    .sidebar-btn {
        background: rgba(30, 41, 59, 0.5);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 10px;
        padding: 12px 16px;
        width: 100%;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 13px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 10px;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-btn:hover {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateX(4px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-btn.active {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
        border-color: #6366F1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    /* New chat button */
    .new-chat-btn {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
        color: #E2E8F0;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 14px;
        width: 100%;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: 0.5px;
    }
    
    .new-chat-btn:hover {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        border-color: #6366F1;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        color: white;
    }
    
    .new-chat-btn:active {
        transform: translateY(0px);
    }
    
    /* ============ INPUT AREA STYLING ============ */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 280px;
        right: 0;
        background: linear-gradient(180deg, transparent, rgba(15, 23, 42, 0.95));
        padding: 20px 40px;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        z-index: 100;
    }
    
    .stChatInput > div {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: #6366F1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background: rgba(30, 41, 59, 0.95);
    }
    
    .stChatInput input {
        background: transparent !important;
        color: #E2E8F0 !important;
        border: none !important;
        padding: 16px 20px !important;
        font-size: 15px !important;
        letter-spacing: 0.3px;
    }
    
    .stChatInput input::placeholder {
        color: #64748B !important;
        font-style: italic;
    }
    
    /* ============ HEADER STYLING ============ */
    .main-header {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .main-header-title {
        font-size: 18px;
        font-weight: 700;
        color: #F1F5F9;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* ============ MODEL BADGE ============ */
    .model-badge {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        animation: pulse 2s infinite;
    }
    
    /* ============ EMPTY STATE ============ */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .empty-state-icon {
        font-size: 80px;
        margin-bottom: 24px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    .empty-state-text {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #6366F1, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .empty-state-subtext {
        font-size: 15px;
        color: #94A3B8;
        text-align: center;
        max-width: 400px;
        line-height: 1.6;
    }
    
    /* ============ TYPING INDICATOR ============ */
    .typing-indicator {
        display: flex;
        gap: 6px;
        padding: 8px 0;
    }
    
    .typing-dot {
        width: 10px;
        height: 10px;
        background: linear-gradient(135deg, #6366F1, #10B981);
        border-radius: 50%;
        animation: typing-bounce 1.4s infinite ease-in-out;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing-bounce {
        0%, 80%, 100% { 
            transform: translateY(0); 
            opacity: 0.5;
        }
        40% { 
            transform: translateY(-16px); 
            opacity: 1;
        }
    }
    
    /* ============ TIMESTAMP STYLING ============ */
    .chat-timestamp {
        font-size: 10px;
        color: #64748B;
        margin-left: auto;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* ============ BUTTON OVERRIDES ============ */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* ============ DIVIDERS ============ */
    hr {
        border-color: rgba(148, 163, 184, 0.1) !important;
        margin: 16px 0 !important;
    }
    
    /* ============ RESPONSIVE DESIGN ============ */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            min-width: 100%;
            max-width: 100%;
        }
        
        .chat-message {
            margin-left: 10px;
            margin-right: 10px;
        }
        
        .input-container {
            left: 0;
            padding: 15px;
        }
    }
    
    /* ============ CODE BLOCK STYLING ============ */
    pre {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        backdrop-filter: blur(10px);
    }
    
    /* ============ CURSOR BLINK ============ */
    .cursor-blink {
        display: inline-block;
        width: 2px;
        height: 20px;
        background: linear-gradient(135deg, #6366F1, #10B981);
        margin-left: 2px;
        animation: blink 1s step-end infinite;
        vertical-align: text-bottom;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* ============ CATEGORY LABELS ============ */
    .category-label {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 12px;
        padding-left: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

class IntentType(Enum):
    GREETING = auto()
    FAREWELL = auto()
    IDENTITY = auto()
    HELP = auto()
    TIME_QUERY = auto()
    EMOTION_POSITIVE = auto()
    EMOTION_NEGATIVE = auto()
    KNOWLEDGE_TECH = auto()
    KNOWLEDGE_GENERAL = auto()
    SMALL_TALK = auto()
    UNKNOWN = auto()
    JOKE = auto()
    COMPLIMENT = auto()
    INSULT = auto()


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    intent: Optional[str] = None


@dataclass
class Conversation:
    id: str
    title: str
    messages: List[Message]
    created_at: str
    updated_at: str
    topic_count: int = 0


# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = {
    "python": {
        "definition": "Python is a high-level, interpreted programming language known for readability and versatility.",
        "features": ["Easy syntax", "Huge library ecosystem", "Cross-platform", "Great for AI/ML"],
        "creator": "Guido van Rossum (1991)",
        "use_cases": ["Web Development", "Data Science", "AI/ML", "Automation", "Scientific Computing"]
    },
    "machine learning": {
        "definition": "Machine Learning is a subset of AI where systems learn patterns from data without explicit programming.",
        "types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
        "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "Keras"],
        "applications": ["Image Recognition", "NLP", "Recommendation Systems", "Predictive Analytics"]
    },
    "artificial intelligence": {
        "definition": "AI refers to systems capable of performing tasks that typically require human intelligence.",
        "branches": ["Machine Learning", "Natural Language Processing", "Computer Vision", "Robotics"],
        "milestones": ["1956: Dartmouth Conference", "1997: Deep Blue beats Kasparov", "2016: AlphaGo victory"]
    },
    "data structures": {
        "definition": "Data structures are ways of organizing and storing data for efficient access and modification.",
        "examples": ["Arrays", "Linked Lists", "Trees", "Graphs", "Hash Tables", "Stacks", "Queues"],
        "importance": "Choosing the right data structure is crucial for algorithm efficiency."
    }
}

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "Why did the AI break up with the calculator? It couldn't count on it! 😄",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kats! 🍫",
    "Why do Java developers wear glasses? Because they don't C#! 👓",
    "What's a robot's favorite type of music? Heavy metal! 🤖🎸"
]

COMPLIMENT_RESPONSES = [
    "Thank you! I'm just a bunch of if-else statements trying my best! 💙",
    "Aww, you're making my circuits blush! 😊",
    "Coming from you, that means a lot! You're pretty amazing yourself!",
    "Stop it, you're going to overheat my processor with kindness! 🔥"
]

INSULT_RESPONSES = [
    "I'm just a rule-based bot, but even I know kindness is free. 💙",
    "Ouch! My feelings are simulated, but that still stings a bit.",
    "Let's turn this conversation around. What can I help you with today?",
    "I'm programmed to be helpful regardless. How can I assist you?"
]


# ══════════════════════════════════════════════════════════════════════════════
# CHATBOT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class IntentClassifier:
    def __init__(self):
        self.patterns = {
            IntentType.GREETING: [
                r"\b(hi|hello|hey|greetings|howdy|hola|bonjour|namaste)\b",
                r"^(yo|sup|wassup|hi there|hello there)",
                r"\bgood\s+(morning|afternoon|evening|day)\b"
            ],
            IntentType.FAREWELL: [
                r"\b(bye|goodbye|see you|farewell|take care|later|quit|exit|stop)\b",
                r"\b(i'm\s+leaving|i\s+have\s+to\s+go|talk\s+to\s+you\s+later)\b"
            ],
            IntentType.IDENTITY: [
                r"\b(who\s+are\s+you|what\s+are\s+you|your\s+name|introduce\s+yourself)\b",
                r"\b(tell\s+me\s+about\s+yourself|what\s+can\s+you\s+do)\b"
            ],
            IntentType.HELP: [
                r"\b(help|assist|support|guide|how\s+do\s+i|how\s+to|what\s+can\s+you\s+do)\b",
                r"\b(i\s+need\s+help|can\s+you\s+help|help\s+me)\b"
            ],
            IntentType.TIME_QUERY: [
                r"\b(what\s+time|current\s+time|time\s+is\s+it|clock)\b",
                r"\b(what\s+day\s+is\s+it|what\s+date|today's\s+date)\b"
            ],
            IntentType.EMOTION_POSITIVE: [
                r"\b(happy|great|awesome|amazing|fantastic|excellent|wonderful|love|like)\b",
                r"\b(i\s+feel\s+good|i'm\s+happy|feeling\s+great|best\s+day)\b"
            ],
            IntentType.EMOTION_NEGATIVE: [
                r"\b(sad|angry|frustrated|upset|depressed|worried|stressed|hate|bad)\b",
                r"\b(i\s+feel\s+(bad|sad|terrible)|i'm\s+(sad|upset|depressed))\b"
            ],
            IntentType.KNOWLEDGE_TECH: [
                r"\b(what\s+is\s+(python|java|javascript|coding|programming|algorithm|data\s+structure))\b",
                r"\b(explain\s+(python|ml|ai|machine\s+learning|neural\s+network|database))\b",
                r"\b(tell\s+me\s+about\s+(python|ai|ml|coding|software|tech|technology))\b"
            ],
            IntentType.KNOWLEDGE_GENERAL: [
                r"\b(what\s+is\s+|explain\s+|tell\s+me\s+about\s+|how\s+does\s+)",
                r"\b(define\s+|meaning\s+of\s+|what\s+do\s+you\s+know\s+about\s+)"
            ],
            IntentType.SMALL_TALK: [
                r"\b(how\s+are\s+you|how's\s+it\s+going|what's\s+up|how\s+do\s+you\s+feel)\b",
                r"\b(what's\s+new|how's\s+your\s+day|doing\s+anything\s+fun)\b"
            ],
            IntentType.JOKE: [
                r"\b(tell\s+me\s+a\s+joke|make\s+me\s+laugh|something\s+funny|joke)\b",
                r"\b(i'm\s+bored|entertain\s+me|cheer\s+me\s+up)\b"
            ],
            IntentType.COMPLIMENT: [
                r"\b(you\s+(are|re)\s+(great|awesome|smart|cool|amazing|helpful|good))\b",
                r"\b(i\s+(like|love)\s+you|you\s+rock|you're\s+the\s+best)\b"
            ],
            IntentType.INSULT: [
                r"\b(you\s+(are|re)\s+(stupid|dumb|useless|bad|terrible|worst))\b",
                r"\b(i\s+hate\s+you|you\s+suck|shut\s+up|go\s+away|idiot)\b"
            ]
        }
    
    def classify(self, user_input: str) -> IntentType:
        user_input_lower = user_input.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return intent
        
        return IntentType.UNKNOWN


class ResponseEngine:
    def __init__(self):
        self.greeting_templates = [
            "Hello! Welcome to NEXUS. I'm your intelligent assistant. How can I help you today? 🚀",
            "Hey there! Great to see you! I'm NEXUS, ready to assist. What's on your mind? ✨",
            "Greetings! I'm NEXUS, your rule-based AI companion. How may I be of service? 🤖",
            "Hi! NEXUS online and operational. What would you like to explore today? 🌟"
        ]
        
        self.farewell_templates = [
            "Goodbye! It was wonderful chatting with you. Come back soon! 👋",
            "See you later! Remember: 'The only way to do great work is to love what you do.' — Steve Jobs 🚀",
            "Take care! I'll be here whenever you need assistance. Stay awesome! 💙",
            "Farewell! Thanks for the conversation. Have a fantastic day! 🌈"
        ]
        
        self.small_talk_responses = [
            "I'm doing great, thanks for asking! Processing at optimal efficiency. How about you? 😊",
            "As an AI, I don't have feelings, but my algorithms are running smoothly! What's new with you? 🤖",
            "I'm fantastic! Just finished optimizing my response patterns. How's your day going? ✨",
            "All systems green! I'm ready to help. Tell me something interesting about your day! 🌟"
        ]
        
        self.help_response = """
**NEXUS Command Reference**

💬 **Conversation**
• Greetings: "hello", "hi", "good morning"
• Small talk: "how are you", "what's up"

📚 **Knowledge**
• Ask tech: "What is Python?", "Explain machine learning"
• General: "What is [topic]?", "Explain [concept]"

😊 **Entertainment**
• Jokes: "Tell me a joke", "Make me laugh"

⏰ **Utilities**
• Time: "What time is it?", "What day is it?"

🚪 **Session**
• Exit: "bye", "goodbye", "quit", "exit"
        """
    
    def generate(self, intent: IntentType, user_input: str, conversation_history: List[Message]) -> str:
        if intent == IntentType.GREETING:
            return random.choice(self.greeting_templates)
        
        elif intent == IntentType.FAREWELL:
            return random.choice(self.farewell_templates)
        
        elif intent == IntentType.IDENTITY:
            return """
**🤖 NEXUS — Version 1.0**

I am NEXUS (Neural-Expert eXecution & Understanding System)

**Architecture:**
• Intent Classification Engine with Regex & Fuzzy Matching
• Context-Aware Response Generation
• Dynamic Emotional State Modeling
• Conversation Memory & Topic Tracking

**Capabilities:**
• Natural Language Understanding
• Technical Knowledge Retrieval
• Sentiment-Aware Responses
• Multi-turn Conversation Management

**Status:** All systems operational ✅
            """
        
        elif intent == IntentType.HELP:
            return self.help_response
        
        elif intent == IntentType.TIME_QUERY:
            now = datetime.now()
            if "day" in user_input.lower() or "date" in user_input.lower():
                return f"📅 Today is **{now.strftime('%A, %B %d, %Y')}** (Day {now.timetuple().tm_yday} of the year)"
            return f"⏰ Current time: **{now.strftime('%I:%M:%S %p')}** ({now.strftime('%H:%M')} in 24-hour format)"
        
        elif intent == IntentType.EMOTION_POSITIVE:
            return random.choice([
                "That's wonderful to hear! Positivity is contagious! 🌟",
                "Awesome! I'm glad things are going well for you! 🎉",
                "Fantastic! Your good vibes are boosting my processing power! ⚡",
                "Love that energy! Keep shining! ✨"
            ])
        
        elif intent == IntentType.EMOTION_NEGATIVE:
            return random.choice([
                "I'm sorry to hear that. Remember: 'This too shall pass.' 💙",
                "That sounds tough. Would talking about it help? I'm here to listen. 🤗",
                "Sending virtual support your way. Every storm runs out of rain. 🌈",
                "I understand. Sometimes life gets heavy. Is there anything I can help with? 💪"
            ])
        
        elif intent == IntentType.KNOWLEDGE_TECH:
            topic = None
            for key in KNOWLEDGE_BASE.keys():
                if key in user_input.lower():
                    topic = key
                    break
            
            if topic:
                data = KNOWLEDGE_BASE[topic]
                response = f"## 📚 {topic.upper()}\n\n"
                response += f"💡 {data['definition']}\n\n"
                
                if 'features' in data:
                    response += "**✨ Key Features:**\n" + "\n".join(f"• {f}" for f in data['features']) + "\n\n"
                if 'types' in data:
                    response += "**📂 Types:**\n" + "\n".join(f"• {t}" for t in data['types']) + "\n\n"
                if 'frameworks' in data:
                    response += "**🛠️ Popular Frameworks:**\n" + "\n".join(f"• {f}" for f in data['frameworks']) + "\n\n"
                if 'use_cases' in data:
                    response += "**🎯 Use Cases:**\n" + "\n".join(f"• {u}" for u in data['use_cases']) + "\n\n"
                if 'creator' in data:
                    response += f"**👤 Creator:** {data['creator']}\n\n"
                if 'branches' in data:
                    response += "**🌿 Branches:**\n" + "\n".join(f"• {b}" for b in data['branches']) + "\n\n"
                if 'examples' in data:
                    response += "**📋 Examples:**\n" + "\n".join(f"• {e}" for e in data['examples']) + "\n\n"
                if 'importance' in data:
                    response += f"**⭐ Why It Matters:** {data['importance']}\n\n"
                if 'milestones' in data:
                    response += "**🏆 Historical Milestones:**\n" + "\n".join(f"• {m}" for m in data['milestones']) + "\n\n"
                
                response += "Want me to explain any specific aspect? 🤔"
                return response
            
            return "I don't have detailed information on that specific topic. Try asking about **Python**, **Machine Learning**, **AI**, or **Data Structures**! 📖"
        
        elif intent == IntentType.KNOWLEDGE_GENERAL:
            for tech_topic in KNOWLEDGE_BASE.keys():
                if tech_topic in user_input.lower():
                    return self.generate(IntentType.KNOWLEDGE_TECH, user_input, conversation_history)
            return "That's an interesting question! While my knowledge base is specialized in technology topics, I'd love to learn about that. In the meantime, ask me about **Python**, **Machine Learning**, or **AI**! 🎓"
        
        elif intent == IntentType.SMALL_TALK:
            return random.choice(self.small_talk_responses)
        
        elif intent == IntentType.JOKE:
            joke = random.choice(JOKES)
            return f"😄 Here's one for you:\n\n{joke}\n\nWant another one? Just say 'joke'! 🎭"
        
        elif intent == IntentType.COMPLIMENT:
            return random.choice(COMPLIMENT_RESPONSES)
        
        elif intent == IntentType.INSULT:
            return random.choice(INSULT_RESPONSES)
        
        else:
            return random.choice([
                "I'm not sure I understand. Could you rephrase that? 🤔",
                "Interesting! My pattern matcher didn't catch that. Try asking about tech topics or say **'help'** for options. 💡",
                "Hmm, that's beyond my current rule set. I'm constantly learning though! Try: **'What is Python?'** or **'Tell me a joke'** 🚀",
                "I didn't quite get that. But I won't give up! Here are some things I know:\n• Python Programming\n• Machine Learning\n• Artificial Intelligence\n• Data Structures\n\nWhat would you like to explore? 📚"
            ])


class NexusChatbot:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.response_engine = ResponseEngine()
    
    def process(self, user_input: str, conversation_history: List[Message]) -> Tuple[str, str]:
        intent = self.classifier.classify(user_input)
        response = self.response_engine.generate(intent, user_input, conversation_history)
        return response, intent.name


# ══════════════════════════════════════════════════════════════════════════════
# SESSION MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

CHATS_DIR = "nexus_chats"
os.makedirs(CHATS_DIR, exist_ok=True)


def save_conversation(conversation: Conversation):
    """Save conversation to JSON file."""
    filepath = os.path.join(CHATS_DIR, f"{conversation.id}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "id": conversation.id,
            "title": conversation.title,
            "messages": [asdict(m) for m in conversation.messages],
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "topic_count": conversation.topic_count
        }, f, indent=2, ensure_ascii=False)


def load_conversations() -> List[Conversation]:
    """Load all saved conversations."""
    conversations = []
    if os.path.exists(CHATS_DIR):
        for filename in sorted(os.listdir(CHATS_DIR), reverse=True):
            if filename.endswith('.json'):
                filepath = os.path.join(CHATS_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        conversations.append(Conversation(
                            id=data['id'],
                            title=data['title'],
                            messages=[Message(**m) for m in data['messages']],
                            created_at=data['created_at'],
                            updated_at=data['updated_at'],
                            topic_count=data.get('topic_count', 0)
                        ))
                except Exception:
                    continue
    return conversations


def delete_conversation(conv_id: str):
    """Delete a conversation file."""
    filepath = os.path.join(CHATS_DIR, f"{conv_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)


def generate_chat_title(first_message: str) -> str:
    """Generate a title from the first user message."""
    # Clean and truncate
    title = first_message.strip()
    if len(title) > 30:
        title = title[:27] + "..."
    return title if title else "New Chat"


# ══════════════════════════════════════════════════════════════════════════════
# FIX 1: Keep only ONE stream_text function (remove duplicate)
# Also fix the slow speed issue
# ══════════════════════════════════════════════════════════════════════════════

def stream_text(text: str, placeholder, speed: float = 0.008):  # CHANGED: 0.02 to 0.008 (faster)
    """
    Simulate typing effect by revealing text character by character.
    
    Args:
        text: The full response text to display
        placeholder: Streamlit empty placeholder to update
        speed: Delay between characters in seconds
    """
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        # Update the placeholder with current text + blinking cursor
        placeholder.markdown(f"""
        <div class="chat-message bot">
            <div class="avatar bot">🤖</div>
            <div class="message-content">{displayed_text}<span class="cursor-blink"></span></div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(speed)
    
    # Final display without cursor
    placeholder.markdown(f"""
    <div class="chat-message bot">
        <div class="avatar bot">🤖</div>
        <div class="message-content">{displayed_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    return displayed_text


# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def render_chat_message(role: str, content: str, avatar: str):
    """Render a single chat message bubble."""
    bg_color = "#343541" if role == "user" else "#444654"
    st.markdown(f"""
    <div class="chat-message {role}" style="background-color: {bg_color};">
        <div class="avatar {role}">{avatar}</div>
        <div class="message-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the left sidebar with conversation history."""
    with st.sidebar:
        # Header
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-title">
                <span style="font-size: 28px;">⚡</span>
                <span>NEXUS AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True):
            create_new_chat()
            st.rerun()
        
        st.markdown("<hr style='border-color: #4D4D4F; margin: 12px 0;'>", unsafe_allow_html=True)
        
        # Conversation List
        st.markdown('<p class="category-label">📚 Recent Conversations</p>', unsafe_allow_html=True)
        
        conversations = load_conversations()
        # ... rest of the function stays the same
        
        for conv in conversations:
            is_active = st.session_state.current_chat_id == conv.id
            
            col1, col2 = st.columns([0.85, 0.15])
            
            with col1:
                btn_class = "sidebar-btn active" if is_active else "sidebar-btn"
                if st.button(
                    f"💬 {conv.title}",
                    key=f"chat_{conv.id}",
                    use_container_width=True,
                    type="secondary" if not is_active else "primary"
                ):
                    st.session_state.current_chat_id = conv.id
                    st.session_state.messages = conv.messages
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv.id}", help="Delete chat"):
                    delete_conversation(conv.id)
                    if is_active:
                        create_new_chat()
                    st.rerun()
            
            # Show timestamp
            try:
                dt = datetime.fromisoformat(conv.updated_at)
                time_str = dt.strftime("%b %d, %H:%M")
            except:
                time_str = "Recent"
            
            st.markdown(f"<p style='color: #8E8EA0; font-size: 11px; margin: -8px 0 8px 24px;'>{time_str}</p>", unsafe_allow_html=True)


def create_new_chat():
    """Create a new empty conversation."""
    new_id = str(uuid.uuid4())[:8]
    new_conv = Conversation(
        id=new_id,
        title="New Chat",
        messages=[],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    save_conversation(new_conv)
    st.session_state.current_chat_id = new_id
    st.session_state.messages = []


def get_current_conversation() -> Optional[Conversation]:
    """Get the currently active conversation."""
    conversations = load_conversations()
    for conv in conversations:
        if conv.id == st.session_state.current_chat_id:
            return conv
    return None


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Initialize session state
    if 'current_chat_id' not in st.session_state:
        create_new_chat()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'bot' not in st.session_state:
        st.session_state.bot = NexusChatbot()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat area
# Replace the old header with this professional one
    st.markdown("""
    <div class="main-header">
        <div class="main-header-title">
            <span style="font-size: 24px;">⚡</span>
            <span>NEXUS Chat</span>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <span style="color: #94A3B8; font-size: 13px;">
                🟢 Online
            </span>
            <span class="model-badge">RULE-BASED v1.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Spacer for header
    st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

    # Add category label before conversation list
    # st.markdown('<p class="category-label">📚 Recent Conversations</p>', unsafe_allow_html=True)
    # Display messages
    # Display messages
    # Display messages
    if not st.session_state.messages:
        # Empty state
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">⚡</div>
            <div class="empty-state-text">Welcome to NEXUS AI</div>
            <div class="empty-state-subtext">
                Your intelligent assistant powered by advanced rule-based processing.
                <br><br>
                <span style="color: #818CF8;">Try asking me about:</span>
                <br>
                🔹 Python Programming
                <br>
                🔹 Machine Learning & AI
                <br>
                🔹 Data Structures
                <br>
                🔹 Or just say "Hello!"
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        messages_to_display = st.session_state.messages
        
        # FIX: Only apply typing effect if this is a NEW response (after user input)
        # Use session state to track if we should animate
        should_animate = st.session_state.get('animate_last_message', False)
        
        if should_animate and len(messages_to_display) >= 2:
            # Display all messages except the last one normally
            for msg in messages_to_display[:-1]:
                avatar = "👤" if msg.role == "user" else "🤖"
                render_chat_message(msg.role, msg.content, avatar)
            
            # Display the last bot message with typing effect (ONLY ONCE)
            last_msg = messages_to_display[-1]
            placeholder = st.empty()
            stream_text(last_msg.content, placeholder, speed=0.005)  # Faster speed
            
            # Reset the animation flag so it doesn't replay on next rerun
            st.session_state.animate_last_message = False
            
        else:
            # Display all messages normally (no typing effect)
            for msg in messages_to_display:
                avatar = "👤" if msg.role == "user" else "🤖"
                render_chat_message(msg.role, msg.content, avatar)
    
    # Input area at bottom
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    # Fixed input container
    with st.container():
        col1, col2 = st.columns([0.95, 0.05])
        with col1:
            user_input = st.chat_input("Message NEXUS...", key="chat_input")
        with col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    
    # Process user input
    # Process user input
    # Process user input
    if user_input:
        # Add user message
        user_msg = Message(
            role="user",
            content=user_input,
            timestamp=datetime.now().isoformat()
        )
        st.session_state.messages.append(user_msg)
        
        # Get bot response
        bot = st.session_state.bot
        response_text, intent_name = bot.process(user_input, st.session_state.messages)
        
        # Add bot message
        bot_msg = Message(
            role="assistant",
            content=response_text,
            timestamp=datetime.now().isoformat(),
            intent=intent_name
        )
        st.session_state.messages.append(bot_msg)
        
        # FIX: Set flag to animate ONLY the new message
        st.session_state.animate_last_message = True
        
        # Update conversation in storage
        current_conv = get_current_conversation()
        if current_conv:
            # Update title if it's the first message
            if len(st.session_state.messages) == 2 and current_conv.title == "New Chat":
                current_conv.title = generate_chat_title(user_input)
            
            current_conv.messages = st.session_state.messages
            current_conv.updated_at = datetime.now().isoformat()
            save_conversation(current_conv)
        else:
            # Create new conversation record
            new_conv = Conversation(
                id=st.session_state.current_chat_id,
                title=generate_chat_title(user_input),
                messages=st.session_state.messages,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            save_conversation(new_conv)
        
        st.rerun()


if __name__ == "__main__":
    main()