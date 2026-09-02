# GitHub Copilot Instructions - Sudoku Project

## Project Goal

This project refactors a legacy Python Sudoku application into a modern Flask-based Sudoku web application.

The goal is to improve the existing project while keeping the code simple, readable, consistent, and maintainable.

## General Coding Style

When helping with this project:

- Write clear and readable code.
- Use meaningful variable and function names.
- Keep functions small and focused.
- Avoid unnecessary complexity.
- Avoid duplicate code.
- Use consistent formatting.
- Add comments only where they are useful.
- Do not add unnecessary libraries or dependencies.
- Keep solutions appropriate for a small student Flask project.
- Prefer simple solutions over overly advanced solutions.

## Refactoring Rules

- Inspect the existing code before modifying it.
- Do not rewrite working legacy code unnecessarily.
- Preserve existing functionality while refactoring.
- Break large or repeated code into reusable functions where appropriate.
- Make changes in manageable steps.
- Do not modify unrelated files.
- Explain important changes before making them.
- Do not add features that are not required by the project.

## Application Structure

Keep responsibilities separated where practical.

### Python / Flask

Python and Flask should handle:

- Sudoku puzzle generation
- Sudoku solving
- Puzzle validation
- Unique-solution checking
- Flask routes
- Backend game logic

### JavaScript

JavaScript should handle:

- User interactions
- Timer
- Immediate input feedback
- Check button behavior
- Hint interactions
- Dark mode
- Local storage
- Top 10 leaderboard display

### CSS

CSS should handle:

- Sudoku grid appearance
- Alternating 3x3 square colors
- Responsive design
- Mobile and desktop layouts
- Light and dark mode styling

## Required Sudoku Features

The completed application must include:

- A 9x9 Sudoku board
- Easy, Medium, and Hard difficulty levels
- Difficulty levels that change the number of prefilled cells
- Puzzles with exactly one unique solution
- Locked prefilled cells
- Immediate visual feedback for invalid moves
- A Check button that highlights incorrect entries
- A Hint button that fills one correct empty cell
- Cells filled using Hint must be locked
- A timer that tracks completion time
- A congratulatory message when the puzzle is solved correctly
- A Top 10 fastest-times leaderboard
- Player name, completion time, difficulty, and hints used in the leaderboard
- Leaderboard data stored using browser localStorage
- A dark mode toggle

## Sudoku Rules

All generated puzzles must follow standard Sudoku rules:

- The board contains 9 rows and 9 columns.
- Numbers range from 1 to 9.
- A number cannot repeat within the same row.
- A number cannot repeat within the same column.
- A number cannot repeat within the same 3x3 box.
- Every generated playable puzzle must have exactly one solution.

## Testing

Testing must be established before major refactoring begins.

Use pytest for Python testing.

When working on the application:

- First create baseline tests for the existing legacy functionality.
- Confirm the initial tests pass before refactoring.
- Preserve existing passing tests.
- Run tests after major refactoring or feature changes.
- Add tests for important game logic where practical.
- Do not change tests simply to make incorrect application code pass.
- Fix the application when a valid test identifies a problem.

## User Interface

The interface should:

- Be simple and readable.
- Work properly on desktop and mobile screens.
- Scale smoothly without visible layout shifts.
- Keep text and controls readable.
- Work correctly in both light and dark modes.
- Clearly distinguish prefilled cells from editable cells.
- Clearly indicate incorrect entries.
- Clearly indicate cells added using the Hint button.
- Use alternating visual styling for the 3x3 Sudoku squares.

## Accessibility

Where practical:

- Use semantic HTML.
- Use clear labels for controls.
- Use readable font sizes.
- Maintain sufficient color contrast.
- Support keyboard interaction.
- Do not rely only on color to communicate important information.

## Copilot Behavior

When assisting with this project:

- Read these instructions before making changes.
- Inspect relevant existing files before proposing modifications.
- Do not invent project requirements.
- Do not invent existing functions, files, or variables.
- Prefer modifying existing code rather than replacing the whole application.
- Explain why significant changes are necessary.
- Prefer the simplest maintainable solution.
- Point out possible problems instead of hiding them.
- Do not add optional features unless specifically requested.
- Follow the project requirements and rubric as the source of truth.

## Responsible Copilot Use

Copilot suggestions must be reviewed before they are accepted.

A suggestion should be rejected or revised if it:

- Adds unnecessary complexity
- Changes unrelated functionality
- Adds unnecessary dependencies
- Conflicts with the project requirements
- Makes the code harder to understand
- Replaces working code without a good reason

Do not automatically accept every suggested change.