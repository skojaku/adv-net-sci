# Assignment Tasks


This assignment requires you to complete two main tasks and submit your work to GitHub. You will need to implement Python functions marked with special comments and create a quiz file with challenging questions that test your understanding of course concepts.

## Task 1: Function Implementation


<p align="center">
  <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgDC8T-6_7wMK9PWpXbRm7FUU2iMMhvAE0YFYX9RcA4PXLGNDJJFW6anUa4tBtIj42AFVQFwI0BN7i4gWNu9ZGcgE-tdx6dbKzvrORIVB9AEyjjdTDkKG4StslIvz8wkHiTiEKORptbXB54/s1600/computer_screen_programming.png" alt="Quiz Dojo" width="30%"/>
</p>

Your first task involves working with the `assignment.py` file using the marimo notebook interface. Throughout this file, you will find functions that are marked with `#TASK` comments in their docstrings. These functions contain placeholder implementations that you need to replace with working code. Each function includes a detailed docstring that specifies the expected input parameters and return values.

## Task 2: Quiz Creation


<p align="center">
  <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlHKrBdBIO7hyuXygw_c4F1vwztHkr9cu9Rssl8c6SDEMBAJzYxsJe2IJsDqgLKU6Qx7GJRBlYqI0zvpbD_LdDbCbux_L3GSjQGX6PhHSYv8nf7-QdO4yjVMTQZr25TfnAwRnOt7NG9l4/s180-c/samurai_kettou.png" alt="Quiz Dojo" width="30%"/>
</p>

Your second task is to create a `quiz.toml` file with exactly two challenging questions about the course material. Here’s the twist: your quiz will be taken by a large language model, not just a human grader. If you can write a question that the LLM gets wrong, you’ll pass this part of the assignment!

To succeed, craft questions that are subtle, require deep understanding, or test tricky edge cases—something that might trip up even a smart AI. Each question should be clearly written in TOML format (see below), and must include a complete, correct answer. Aim for questions that go beyond surface-level facts and require careful reasoning or attention to detail.

**Required format for quiz.toml:**
```toml
[[questions]]
question = "Your first challenging question?"
answer = "Complete and accurate answer."

[[questions]]
question = "Your second challenging question?"
answer = "Complete and accurate answer."
```

**Donts:**
- Do not include heavy mathematical derivations or off-topic content in your quiz questions.
- Do not explicitly instruct the LLM to answer incorrectly.

## Submission Process

Once you have completed both tasks, you need to upload your work to your GitHub repository. Use the standard git command or alternatively web interface. See [how to upload your assingment](https://docs.google.com/presentation/d/19Zvrp5kha6ohF4KvTX9W2jodKkfmsOrJfEZtO_Wg0go)

GitHub Classroom will automatically detect your submission and begin the grading process.


**Tips:**: It is tiresome to go back and forth between the file and the report in GitHub Actions. To save your time, prepare two web browsers side by side, one for the file and one for the GitHub Actions Report. If you are using VSCode, [GitHubAction extension is a good choice](https://open-vsx.org/extension/GitHub/vscode-github-actions).


## Grading and Requirements

Your submission will be automatically graded using GitHub Actions. The grading system will test your function implementations for correctness and validate your quiz questions for relevance to the course material. All functions marked with `#TASK` must be implemented correctly to pass the function portion of the assignment. Your quiz must contain exactly two questions in the proper TOML format, and the questions should be challenging but directly related to course concepts.

**Important Note on Final Grading:** The final grade shown in GitHub Actions will be taken as your final grade for this assignment. The quiz evaluation process can be stochastic, meaning that different evaluation runs may lead to slightly different results due to the AI's variability. However, if you create a well-crafted question with a correct answer, the impact of this variability is negligible. Your goal should be to create questions that are so cleverly designed that the LLM consistently gets them wrong, regardless of minor variations in the evaluation process.
