curl -X POST https://chat.binghamton.edu/api/chat/completions \
-H "Authorization: Bearer sk-7b747530179c4cc992159b7aaec18155" \
-H "Content-Type: application/json" \
-d '{
      "model": "llama3.2:latest",
      "messages": [
        {
          "role": "user",
          "content": "Why is the sky blue?"
        }
      ]
    }'

