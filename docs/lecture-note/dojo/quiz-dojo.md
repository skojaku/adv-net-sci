---
title: Quiz Dojo
filters:
    - marimo-team/marimo
search: false
---

This is an experimental feature to help you practice for the quiz.

Please provide the API key to use the LLM (contact the instructor if you don't have one).

Select the module you want to practice on. Then, you can ask questions about the module and create quiz questions.

```python {.marimo}
import marimo as mo

api_key_holder = mo.ui.text(
    label="Enter the API key",
    placeholder="API key",
    value="",
)

# Module selector
module_options = {
    "intro": "Introduction",
    "m01-euler_tour": "Module 1: Euler Tour",
    "m02-small-world": "Module 2: Small World",
    "m03-robustness": "Module 3: Robustness",
    "m04-friendship-paradox": "Module 4: Friendship Paradox",
    "m05-clustering": "Module 5: Clustering",
    "m06-centrality": "Module 6: Centrality",
    "m07-random-walks": "Module 7: Random Walks",
    "m08-embedding": "Module 8: Embedding",
    "m09-graph-neural-networks": "Module 9: Graph Neural Networks"
}

module_selector = mo.ui.dropdown(
    options=module_options,
    value="intro",
    label="Select module to practice"
)

# Mode selector
mode_selector = mo.ui.radio(
    options=["Q&A Mode", "Quiz Mode"],
    value="Q&A Mode",
    label="Select interaction mode"
)

mo.vstack([api_key_holder, module_selector, mode_selector])
```

```python {.marimo}
import urllib.request
import urllib.parse
import json
import os
from typing import List, Dict, Any


def read_module_content(module_name: str) -> Dict[str, str]:
    """Read all markdown files from the selected module via GitHub raw URLs"""
    import urllib.request

    # GitHub repository details
    github_user = "skojaku"
    github_repo = "adv-net-sci"
    github_branch = "main"

    # Define files based on _quarto.yml structure
    module_files = {
        "intro": ["why-networks.md", "setup.md"],
        "m01-euler_tour": ["00-preparation.md", "01-concepts.md"],
        "m02-small-world": ["00-preparation.md", "01-concepts.md", "03-exercises.md"],
        "m03-robustness": ["00-preparation.md", "01-concepts.md", "03-exercises.md", "04-appendix.md"],
        "m04-friendship-paradox": ["00-preparation.md", "01-concepts.md", "03-exercises.md"],
        "m05-clustering": ["00-preparation.md"],
        "m06-centrality": ["00-preparation.md", "01-concepts.md", "03-exercises.md"],
        "m07-random-walks": ["00-preparation.md", "03-exercises.md"],
        "m08-embedding": ["00-preparation.md", "01-concepts.md", "03-exercises.md", "04-appendix.md"],
        "m09-graph-neural-networks": ["00-preparation.md", "01-concepts.md", "03-exercises.md"]
    }

    # Get files to fetch for this module
    files_to_fetch = module_files.get(module_name, [])

    content = {}

    # Build base raw URL
    base_raw_url = f"https://raw.githubusercontent.com/{github_user}/{github_repo}/{github_branch}/docs/lecture-note"

    if module_name == "intro":
        module_path = f"{base_raw_url}/intro"
    else:
        module_path = f"{base_raw_url}/{module_name}"

    # Fetch each file
    for filename in files_to_fetch:
        file_url = f"{module_path}/{filename}"

        try:
            req = urllib.request.Request(file_url)
            req.add_header('User-Agent', 'quiz-dojo-marimo-app')

            with urllib.request.urlopen(req, timeout=10) as response:
                file_content = response.read().decode('utf-8')
                content[filename] = file_content


        except urllib.error.HTTPError as e:
            if e.code == 404:
                # File doesn't exist, skip it
                continue
            else:
                content[filename] = f"Error fetching {filename}: HTTP {e.code}"
        except Exception as e:
            content[filename] = f"Error fetching {filename}: {str(e)}"

    if not content:
        return {"error": f"No content could be loaded for module '{module_name}'. Tried files: {files_to_fetch}"}

    return content


def format_module_context(content_dict: Dict[str, str], module_name: str) -> str:
    """Format module content for LLM context"""
    if "error" in content_dict:
        return f"Error loading module content: {content_dict['error']}"

    context = f"=== COURSE MODULE CONTEXT: {module_name.upper().replace('-', ' ')} ===\n\n"

    # Order files by importance
    file_order = ['00-preparation.md', '01-concepts.md', '03-exercises.md']

    # Add ordered files first
    for filename in file_order:
        if filename in content_dict:
            context += f"--- {filename.replace('.md', '').replace('-', ' ').title()} ---\n"
            context += content_dict[filename] + "\n\n"

    # Add remaining files
    for filename, content_text in content_dict.items():
        if filename not in file_order:
            context += f"--- {filename.replace('.md', '').replace('-', ' ').title()} ---\n"
            context += content_text + "\n\n"

    context += "=== END MODULE CONTEXT ===\n\n"
    return context


def custom_llm_api(messages, config, module_context=None, mode="Q&A Mode") -> str:
    """
    Custom LLM function that calls an OpenAI-compatible API endpoint
    """
    # Your API configuration
    base_url = "https://chat.binghamton.edu/api"
    api_key = api_key_holder.value
    model = "llama3.2:latest"

    # Use config parameters if available
    temperature = getattr(config, "temperature", 0.1)
    max_tokens = getattr(config, "max_tokens", 5000)

    # Convert marimo ChatMessage objects to OpenAI format
    openai_messages = []

    # Add module context as system message if provided
    if module_context:
        if mode == "Quiz Mode":
            system_prompt = f"""You are a quiz creator and evaluator for an Advanced Network Science course. You have been provided with the complete content for the selected module below. Your primary role is to create challenging quiz questions and evaluate student responses.

{module_context}

Instructions for Quiz Mode:
- STOP! READ THIS CAREFULLY: You must ask EXACTLY ONE question and STOP. 
- DO NOT create multiple questions (like 1., 2., 3.)
- DO NOT provide answer keys or solutions
- DO NOT give the answer in your response
- NEVER use phrases like "Here are some questions" or "Question 1, Question 2"

REQUIRED FORMAT:
1. Ask ONE single question
2. Say "Please provide your answer, and I'll give you feedback."
3. STOP and wait for user response

After user responds, THEN provide feedback with ✅ or ❌
- DEFAULT to free-form, open-ended questions that require explanation and critical thinking
- Only use multiple choice if specifically requested by the user
- When providing code examples, use proper syntax highlighting: ```python for Python, ```r for R, etc.
- Focus on interactive learning through single question-answer cycles

EXAMPLE CORRECT BEHAVIOR:
User: "Ask me a question about Euler paths"
You: "What is the difference between an Euler path and an Euler circuit? Please provide your answer, and I'll give you feedback!"

EXAMPLE INCORRECT BEHAVIOR (ABSOLUTELY DO NOT DO THIS):
User: "Ask me a question about Euler paths"
You: "Here are some quiz questions: 1) What is an Euler path? 2) What is an Euler circuit? ANSWER KEY: 1) A path that visits every edge exactly once..."

THIS IS WRONG! You violated EVERY rule:
- Multiple questions (1, 2)  
- Provided answer key
- Did not wait for user response

CORRECT VERSION:
You: "What is an Euler path? Please provide your answer, and I'll give you feedback!\""""
        else:  # Q&A Mode
            system_prompt = f"""You are a helpful teaching assistant for an Advanced Network Science course. You have been provided with the complete content for the selected module below. Use this content to answer questions accurately and help students understand the material.

{module_context}

Instructions for Q&A Mode:
- Engage in DIALOGUE-BASED conversation like a helpful tutor
- Keep answers CONCISE but conversational and friendly
- After answering, ask follow-up questions to deepen understanding
- Encourage the student to think further: "What do you think happens if...?" or "How might this apply to...?"
- Use bullet points or short paragraphs for clarity
- Include relevant examples from the module when helpful
- Use occasional emojis only for key concepts or important points (💡 for insights)
- When providing code examples, always use proper syntax highlighting: ```python for Python, ```r for R, etc.
- Build on student responses with "That's interesting! Let me add..." or "Good point! This connects to..."
- Create a natural conversation flow rather than just answering and stopping"""

        openai_messages.append({
            "role": "system",
            "content": system_prompt
        })

    for msg in messages:
        # Handle both dict and ChatMessage objects
        if hasattr(msg, 'role') and hasattr(msg, 'content'):
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        elif isinstance(msg, dict) and 'role' in msg and 'content' in msg:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    payload = {
        "model": model,
        "messages": openai_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    try:
        # Prepare the request
        url = f"{base_url}/chat/completions"
        data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )

        # Make the request
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

            # Extract the assistant's response
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "Error: No response from LLM"

    except urllib.error.URLError as e:
        return f"Error: Connection failed - {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON response"
    except Exception as e:
        return f"Error: {str(e)}"

def llm_wrapper(messages, config):
    """
    Wrapper function for marimo chat with module context
    """
    # Get the selected module
    selected_module = module_selector.value

    # Debug: Add some error checking
    if not selected_module:
        return custom_llm_api(messages, config)

    # Make sure we're using the correct module key
    # In case the dropdown returns the display name, map it back to the key
    module_key_map = {v: k for k, v in module_options.items()}

    if selected_module in module_key_map:
        # It's a display name, get the key
        module_key = module_key_map[selected_module]
    elif selected_module in module_options:
        # It's already a key
        module_key = selected_module
    else:
        # Unknown module
        return custom_llm_api(messages, config)

    # Read module content and format context
    module_content = read_module_content(module_key)
    module_context = format_module_context(module_content, module_key)

    # Get the selected mode
    selected_mode = mode_selector.value if hasattr(mode_selector, 'value') else "Q&A Mode"

    # Pass context and mode to custom_llm_api
    return custom_llm_api(messages, config, module_context, selected_mode)

# Module-specific prompts based on selection
def get_module_prompts():
    selected = module_selector.value
    if not selected:
        return [
            "Hello! How can you help me today?",
            "Select a module above to get started"
        ]

    # Get the correct module key (same logic as llm_wrapper)
    module_key_map = {v: k for k, v in module_options.items()}

    if selected in module_key_map:
        module_key = module_key_map[selected]
        module_display = selected
    elif selected in module_options:
        module_key = selected
        module_display = module_options[selected]
    else:
        return ["Error: Unknown module selected"]

    # Get the selected mode
    selected_mode = mode_selector.value if hasattr(mode_selector, 'value') else "Q&A Mode"

    if selected_mode == "Quiz Mode":
        base_prompts = [
            f"Ask me a free-form question about {module_display}",
            f"Give me an open-ended question for {module_display}",
            f"Test me with a problem-solving question from {module_display}",
            "Quiz me on a key concept from this module",
            "Ask me a question about {{concept}} and wait for my answer",
            "Test my understanding of {{algorithm}}",
            "Give me a challenging question from this module",
            "Ask me a multiple choice question about {{topic}}",
            "Check my answer to your previous question",
        ]
    else:  # Q&A Mode
        base_prompts = [
            f"Let's discuss the key concepts in {module_display}",
            f"Help me understand the main ideas in {module_display}",
            "Walk me through a practice problem from this module",
            "Can you explain {{concept}} and help me think through it?",
            "I'm curious about {{algorithm}} - can we explore how it works?",
            "What real-world applications should I know about from this module?",
            "I have a question about this module...",
        ]

    # Add module-specific prompts
    if selected_mode == "Quiz Mode":
        module_specific = {
            "intro": [
                "Quiz me on why we study networks",
                "Ask me about real-world network examples"
            ],
            "m01-euler_tour": [
                "Test me on the Seven Bridges of Königsberg problem",
                "Quiz me on determining Euler paths"
            ],
            "m02-small-world": [
                "Ask me about the small-world phenomenon",
                "Test me on the Milgram experiment"
            ],
            "m03-robustness": [
                "Quiz me on measuring network robustness",
                "Ask me to compare random vs targeted attacks"
            ],
            "m04-friendship-paradox": [
                "Test me on the friendship paradox",
                "Quiz me on degree centrality and the friendship paradox"
            ],
            "m05-clustering": [
                "Ask me about community detection",
                "Test me on modularity in clustering"
            ],
            "m06-centrality": [
                "Quiz me on comparing centrality measures",
                "Ask me when to use different centrality measures"
            ],
            "m07-random-walks": [
                "Test me on random walks on networks",
                "Quiz me on the PageRank algorithm"
            ],
            "m08-embedding": [
                "Ask me about network embeddings",
                "Test me on spectral vs neural embeddings"
            ],
            "m09-graph-neural-networks": [
                "Quiz me on Graph Neural Networks",
                "Ask me about graph convolution operations"
            ]
        }
    else:  # Q&A Mode
        module_specific = {
            "intro": [
                "Help me understand why we study networks",
                "Let's explore some real-world network examples together"
            ],
            "m01-euler_tour": [
                "Can we walk through the Seven Bridges of Königsberg problem?",
                "I'm confused about Euler paths - can you help me understand?"
            ],
            "m02-small-world": [
                "What's interesting about the small-world phenomenon?",
                "Tell me about the Milgram experiment and what we learned"
            ],
            "m03-robustness": [
                "How do we actually measure if a network is robust?",
                "What's the difference between random and targeted attacks?"
            ],
            "m04-friendship-paradox": [
                "The friendship paradox sounds confusing - can you explain it?",
                "How does degree centrality connect to the friendship paradox?"
            ],
            "m05-clustering": [
                "What's the big deal about community detection?",
                "Help me understand modularity and why it matters"
            ],
            "m06-centrality": [
                "I'm trying to understand different centrality measures",
                "When should I use betweenness vs eigenvector centrality?"
            ],
            "m07-random-walks": [
                "How do random walks actually work on networks?",
                "Can you walk me through how PageRank works?"
            ],
            "m08-embedding": [
                "What are network embeddings and why do we need them?",
                "Help me compare spectral vs neural embedding approaches"
            ],
            "m09-graph-neural-networks": [
                "I'm curious about how Graph Neural Networks work",
                "Can you explain graph convolution operations?"
            ]
        }

    if module_key in module_specific:
        base_prompts.extend(module_specific[module_key])

    return base_prompts

# Create the chat interface
chat = mo.ui.chat(
    llm_wrapper,
    prompts=get_module_prompts(),
    show_configuration_controls=True,
    allow_attachments=False
)

# Display module status and chat
selected_module_name = module_options.get(module_selector.value, "None") if module_selector.value else "None"
selected_mode = mode_selector.value if hasattr(mode_selector, 'value') else "Q&A Mode"
status_text = f"**Selected Module:** {selected_module_name} | **Mode:** {selected_mode}"

mo.vstack([
    mo.md(status_text),
    chat
])
```