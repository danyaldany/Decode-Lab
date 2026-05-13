# NEXUS AI 🤖⚡

A professional **Rule-Based AI Chatbot** built with Streamlit featuring a modern ChatGPT-style interface, conversation history, intent classification, animated responses, and a responsive UI.

---

## 📌 Overview

NEXUS AI is an advanced **rule-based chatbot system** designed to simulate intelligent conversations using:

* Regex-based intent classification
* Dynamic response generation
* Conversation memory
* Persistent chat history
* Modern futuristic UI
* Typing animations
* Knowledge base support

This project demonstrates how a chatbot can be built **without machine learning**, using carefully designed rules and patterns.

---

# ✨ Features

## 🎨 Professional UI

* ChatGPT-inspired interface
* Dark futuristic theme
* Responsive design
* Animated chat bubbles
* Custom scrollbar styling
* Typing indicator animation

---

## 🧠 Intelligent Intent Detection

The chatbot can detect:

* Greetings
* Farewells
* Help requests
* Emotional states
* Technical questions
* Small talk
* Jokes
* Compliments
* Insults

---

## 💾 Persistent Chat History

* Saves conversations as JSON
* Sidebar conversation history
* Load previous chats
* Delete chats
* Auto-generated chat titles

---

## 📚 Built-in Knowledge Base

Supports technical topics like:

* Python
* Artificial Intelligence
* Machine Learning
* Data Structures

---

## ⚡ Typing Animation

* Simulated real-time typing
* Streaming text effect
* Cursor animation

---

## 🛠️ Tech Stack

| Technology   | Purpose               |
| ------------ | --------------------- |
| Python       | Backend Logic         |
| Streamlit    | Web Interface         |
| Regex (`re`) | Intent Classification |
| JSON         | Chat Storage          |
| CSS          | Professional Styling  |
| UUID         | Unique Chat IDs       |

---

# 📂 Project Structure

```bash
NEXUS-AI/
│
├── app.py
├── nexus_chats/
│   ├── chat1.json
│   ├── chat2.json
│
├── README.md
```

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/nexus-ai.git
cd nexus-ai
```

---

## 2️⃣ Install Dependencies

```bash
pip install streamlit
```

---

## 3️⃣ Run Application

```bash
streamlit run app.py
```

---

# 🖥️ How It Works

---

## 1. User Sends Message

Example:

```text
What is Python?
```

---

## 2. Intent Classifier Detects Intent

Using regex patterns:

```python
r"\b(what\s+is\s+(python|java|javascript))\b"
```

Intent detected:

```text
KNOWLEDGE_TECH
```

---

## 3. Response Engine Generates Reply

The chatbot retrieves information from the knowledge base and generates a structured response.

---

# 🧩 Core Components

---

## 🔹 IntentClassifier

Responsible for:

* Pattern matching
* Detecting user intent
* Regex processing

### Example

```python
IntentType.GREETING
IntentType.JOKE
IntentType.HELP
```

---

## 🔹 ResponseEngine

Generates chatbot responses based on:

* Intent
* User input
* Conversation history

---

## 🔹 NexusChatbot

Main chatbot controller.

Handles:

* Intent classification
* Response generation
* Conversation flow

---

## 🔹 Session Management

Functions include:

```python
save_conversation()
load_conversations()
delete_conversation()
```

---

# 🎯 Supported Intents

| Intent            | Example           |
| ----------------- | ----------------- |
| Greeting          | "hello"           |
| Farewell          | "bye"             |
| Help              | "help me"         |
| Joke              | "tell me a joke"  |
| Tech Knowledge    | "What is Python?" |
| Small Talk        | "how are you?"    |
| Emotion Detection | "I feel sad"      |

---

# 💡 Example Conversation

```text
User: What is Machine Learning?

NEXUS:
Machine Learning is a subset of AI where systems learn patterns from data without explicit programming.
```

---

# 🎨 UI Highlights

## Custom CSS Features

* Glassmorphism effects
* Gradient backgrounds
* Animated avatars
* Hover effects
* Smooth transitions

---

# 📦 Data Storage

Chats are stored locally as:

```json
{
  "id": "123abc",
  "title": "What is Python?",
  "messages": [],
  "created_at": "...",
  "updated_at": "..."
}
```

---

# 🔥 Future Improvements

Planned upgrades:

* OpenAI API integration
* Voice input support
* Speech synthesis
* Database integration
* Authentication system
* Multi-language support
* AI memory system
* Semantic search
* LLM integration

---

# 🧪 Example Commands

## General

```text
hello
how are you
tell me a joke
```

## Technical

```text
What is AI?
Explain Python
Tell me about machine learning
```

---

# 📈 Learning Objectives

This project helps understand:

* Rule-based chatbots
* NLP basics
* Regex pattern matching
* Streamlit development
* UI/UX design
* State management
* JSON data handling

---

# 🏗️ Architecture

```text
User Input
    ↓
Intent Classifier
    ↓
Response Engine
    ↓
Knowledge Base
    ↓
Bot Response
```

---

# ⚠️ Limitations

Since NEXUS is rule-based:

* Cannot truly understand language
* No machine learning
* Limited flexibility
* Responses depend on predefined rules

---

# 🤝 Contributing

Contributions are welcome.

You can improve:

* UI design
* Intent accuracy
* Knowledge base
* Performance
* Features

---

---

# 👨‍💻 Author

**Danyal Arshad**
BS Computer Science Student

---

