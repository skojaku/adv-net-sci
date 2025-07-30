---
title: Quiz Dojo
filters:
    - marimo-team/marimo
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

mo.vstack([api_key_holder, module_selector])
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


def custom_llm_api(messages, config, module_context=None) -> str:
    """
    Custom LLM function that calls an OpenAI-compatible API endpoint
    """
    # Your API configuration
    base_url = "https://chat.binghamton.edu/api"
    api_key = api_key_holder.value
    model = "llama3.2:latest"

    # Use config parameters if available
    temperature = getattr(config, "temperature", 0.7)
    max_tokens = getattr(config, "max_tokens", 1000)

    # Convert marimo ChatMessage objects to OpenAI format
    openai_messages = []
    
    # Add module context as system message if provided
    if module_context:
        openai_messages.append({
            "role": "system",
            "content": f"""You are a helpful teaching assistant for an Advanced Network Science course. You have been provided with the complete content for the selected module below. Use this content to answer questions accurately and create relevant quiz questions.

{module_context}

Instructions:
- Answer questions based on the module content provided above
- When creating quiz questions, make them relevant to the concepts in this module
- Reference specific concepts, algorithms, or examples from the module when helpful
- If asked about topics not covered in this module, politely redirect to the module content"""
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
    
    # Pass context to custom_llm_api
    return custom_llm_api(messages, config, module_context)

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
    
    base_prompts = [
        f"Explain the key concepts in {module_display}",
        f"Create a quiz question about {module_display}",
        "What are the main learning objectives for this module?",
        "Give me a practice problem from this module",
        "Explain {{concept}} from this module in simple terms",
        "How does {{algorithm}} work in network analysis?",
    ]
    
    # Add module-specific prompts
    module_specific = {
        "intro": [
            "Why do we study networks?",
            "What are some examples of real-world networks?"
        ],
        "m01-euler_tour": [
            "Explain the Seven Bridges of Königsberg problem",
            "How do you determine if a graph has an Euler path?"
        ],
        "m02-small-world": [
            "What is the small-world phenomenon?",
            "Explain the Milgram experiment"
        ],
        "m03-robustness": [
            "How do we measure network robustness?",
            "What is the difference between random and targeted attacks?"
        ],
        "m04-friendship-paradox": [
            "Explain the friendship paradox",
            "How does degree centrality relate to the friendship paradox?"
        ],
        "m05-clustering": [
            "What is community detection?",
            "Explain modularity and its role in clustering"
        ],
        "m06-centrality": [
            "Compare different centrality measures",
            "When would you use betweenness vs eigenvector centrality?"
        ],
        "m07-random-walks": [
            "How do random walks work on networks?",
            "Explain PageRank algorithm"
        ],
        "m08-embedding": [
            "What are network embeddings?",
            "Compare spectral vs neural embedding methods"
        ],
        "m09-graph-neural-networks": [
            "How do Graph Neural Networks work?",
            "Explain graph convolution operations"
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
status_text = f"**Selected Module:** {selected_module_name}"

mo.vstack([
    mo.md(status_text),
    chat
])
```