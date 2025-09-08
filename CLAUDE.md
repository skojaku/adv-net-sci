# Sadamori Kojaku's Slide Writing Style Guide

## Interactive Teaching Philosophy
When creating slides for Sadamori, follow his interactive, step-by-step narrative approach:
- **Context → Question → Discussion → Content** pattern throughout
- Include specific prompts for student interaction ("Turn to your neighbor", "Take 30 seconds")
- Break down complex concepts into smaller interactive segments
- Add thought experiments and real-time questioning
- Create multiple discussion points and student participation moments

## Slide Structure & Design Patterns

### 1. Question-Answer Flow
Use structured callout boxes for pedagogical flow:
```markdown
::: {.callout-note title = "Question:"}
[Thought-provoking question or scenario]
:::

Think about it... discuss with your neighbor for 30 seconds

::: {.incremental}
- **Your predictions:**
  - Option A?
  - Option B? 
  - Option C?
- *Let's hear some thoughts...*
:::

## Answer

::: {.callout-tip title = "Answer:"}
- First: [Specific fact]
- Second: **[Emphasized fact]**
:::
```

### 2. Two-Column Layouts
Use sophisticated column layouts to balance text and visuals:
```markdown
:::: {.columns}

::: {.column width="70%"}
[Main content, questions, or explanations]
:::

::: {.column width="30%"}
![](image.jpg){width=50% fig-align="center"}
:::

::::
```

Common width ratios:
- 70/30 for text-heavy with small supporting image
- 50/50 for equal balance
- 40/60 for image-heavy with minimal text

### 3. Progressive Reveals
Use incremental display for building suspense:
```markdown
::: {.incremental}
- Point 1
- Point 2  
- *Italicized interaction cue*
:::
```

### 4. Image Handling
**Prefer Quarto syntax over HTML:**
```markdown
![](url){width=80% fig-align="center"}
```
**Instead of:**
```html
<img src="url" style="width: 80%;">
```

**Use local lecture note figures when possible:**
- Path: `../lecture-note/m01-euler_tour/tikz-tex/[hash]/[hash].svg`
- Path: `../lecture-note/figs/[filename].jpg`

### 5. Content Style

#### Specific Facts Over Generalities
- ✅ "First: United States, Second: **Spain**"  
- ❌ "Disease spread to nearby countries"

#### Personal References
- Add personality: "Alien scientist (like von Neumann!)"
- Include historical context and memorable details

#### Interactive Prompts
- "Take 30 seconds"
- "Turn to your neighbor"
- "Raise your hands"
- "Let's count together"
- "What strategies did you come up with?"

## Technical Specifications

### Slide Headers
```yaml
---
title: "Module: Topic"
author: "Sadamori Kojaku"  
format:
  revealjs:
    slide-number: true
    chalkboard:
      buttons: false
    preview-links: auto
    theme: simple
    css: css/style.css
---
```

### Section Separators
Use `##` for slide breaks, not `---`

### Visual Hierarchy
- `#` for major section headers
- `##` for slide titles
- `**Bold**` for key terms and emphasis
- `*Italic*` for interaction cues and asides

## Pedagogical Patterns

### 1. Storytelling Opening
Start with concrete, memorable stories:
```markdown
## Let's start with a story... 🦠

::: {.callout-note title = "Question:"}
2009: H1N1 pandemic spreads globally
Do you remember which countries were infected first?
:::
```

### 2. Thought Experiments
Frame abstract concepts through relatable scenarios:
```markdown
::: {.callout-note title = "Question:"}
Imagine you're an Alien scientist studying humans...
You understand every single neuron perfectly.
Can you predict what they'll dream about?
:::
```

### 3. Progressive Complexity
- Start with familiar examples
- Build to abstract concepts
- Always return to practical applications

### 4. Visual-First Design
- Large, compelling figures (80-100% width)
- Minimal text overlaying images
- Strategic use of white space
- Consistent visual theme using course figures

## Content Philosophy

### Interactive Over Instructive
- Pose questions before giving answers
- Create anticipation and engagement
- Students construct knowledge through guided discovery

### Concrete Over Abstract  
- Start with specific examples before generalizing
- Use memorable facts and figures
- Connect to students' daily experiences

### Visual Over Verbal
- Let images drive the narrative
- Use text to complement, not compete with visuals
- Create visual-textual harmony through columns

## Example Complete Pattern
```markdown
## Topic Introduction 🎯

::: {.callout-note title = "Question:"}
[Engaging question or scenario]
:::

*Interaction prompt*

::: {.incremental}
- **Your predictions:**
  - Option A?
  - Option B?
- *Let's discuss...*
:::

## Answer

:::: {.columns}

::: {.column width="60%"}

::: {.callout-tip title = "Answer:"}
[Specific factual answer]
:::

**Follow-up question for deeper thinking**

:::

::: {.column width="40%"}
![](relevant-image.svg){width=90% fig-align="center"}
:::

::::
```

Always prioritize student engagement, visual appeal, and step-by-step knowledge construction following this established pattern.