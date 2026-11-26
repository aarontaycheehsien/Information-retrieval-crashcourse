\# Repository working rules



\## Commit every completed change



When you modify repository files, finish the task by committing your changes.



\- Treat a request to edit files as authorization to create a local Git commit.

\- Commit each coherent change after completing relevant checks.

\- Before committing, review the diff and stage only files belonging to your task.

\- Preserve unrelated changes made by the user or another agent. Never include

&#x20; them in your commit without explicit authorization.

\- Use a concise commit message describing the change.

\- Do not amend existing commits, rewrite history, merge branches, or push

&#x20; remotely unless explicitly requested.

\- If checks fail, fix the problem before committing. If you cannot finish,

&#x20; preserve the work and explain why it remains uncommitted.

\- In the final response, report the commit hash, relevant verification results,

&#x20; and any changes left uncommitted.

\- Read-only reviews and tasks that produce no file changes need no commit.



An explicit user instruction such as “do not commit” overrides this default.



\## Editing the book

- The book's source is the Markdown in `book/`. Edit those files, never
  `search-textbook.html` or `read-this-first.html`, which are built and are
  replaced by the next build.
- After editing, run `python tools/build-book.py`, then
  `python tools/build-book.py --check`, and commit the sources together with the
  rebuilt pages. Conventions are in `reviews/markdown-mapping-spec.md`.
- Do not run `tools/markdown/html_to_md.py --book book`: it would overwrite
  authored Markdown, and it refuses while `book/book.json` says `"markdown"`.

## Parallel development



\- Work in the development worktree assigned to the current task.

\- Confirm the working directory and branch before editing.

\- Do not switch branches or change another worktree as part of ordinary edits.

\- Commit locally on the current development branch; merging back is a separate

&#x20; action requiring an explicit request.

