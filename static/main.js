// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_KEY = 'sudoku-leaderboard-top-10';
const THEME_KEY = 'sudoku-theme';
let puzzle = [];
let solution = [];
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerInterval = null;
let currentGameId = null;
let completedGameSubmitted = false;

function setTheme(isDark) {
  document.body.dataset.theme = isDark ? 'dark' : 'light';
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.textContent = isDark ? 'Light Mode' : 'Dark Mode';
    toggle.setAttribute('aria-pressed', String(isDark));
  }

  try {
    localStorage.setItem(THEME_KEY, isDark ? 'dark' : 'light');
  } catch (error) {
    // Ignore storage issues and keep the UI functional.
  }
}

function initializeTheme() {
  try {
    const savedTheme = localStorage.getItem(THEME_KEY);
    const prefersDark = savedTheme ? savedTheme === 'dark' : window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(prefersDark);
  } catch (error) {
    setTheme(false);
  }

  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const nextTheme = document.body.dataset.theme !== 'dark';
      setTheme(nextTheme);
    });
  }
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText = 'Time: ' + formatTime(elapsedSeconds);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function getBoardFromInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];

  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const value = inputs[idx].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }

  return board;
}

function hasConflict(board, row, col, value) {
  for (let x = 0; x < SIZE; x++) {
    if (x !== col && board[row][x] === value) {
      return true;
    }
  }

  for (let y = 0; y < SIZE; y++) {
    if (y !== row && board[y][col] === value) {
      return true;
    }
  }

  const startRow = Math.floor(row / 3) * 3;
  const startCol = Math.floor(col / 3) * 3;
  for (let r = startRow; r < startRow + 3; r++) {
    for (let c = startCol; c < startCol + 3; c++) {
      if ((r !== row || c !== col) && board[r][c] === value) {
        return true;
      }
    }
  }

  return false;
}

function refreshImmediateValidation() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');

  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) {
      inp.classList.remove('invalid');
      continue;
    }

    const value = inp.value;
    inp.classList.remove('invalid');
    if (!value) {
      continue;
    }

    const row = Number(inp.dataset.row);
    const col = Number(inp.dataset.col);
    const board = getBoardFromInputs();
    if (hasConflict(board, row, col, parseInt(value, 10))) {
      inp.classList.add('invalid');
    }
  }
}

function setBoxShadeClass(input, row, col) {
  const shadeClass = (Math.floor(row / 3) + Math.floor(col / 3)) % 2 === 0 ? 'box-light' : 'box-dark';
  input.classList.add(shadeClass);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      setBoxShadeClass(input, i, j);
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        document.getElementById('message').innerText = '';
        refreshImmediateValidation();

        const board = getBoardFromInputs();
        if (boardIsComplete(board) && solution.length > 0) {
          const solved = board.every((row, rowIndex) => row.every((value, colIndex) => value === solution[rowIndex][colIndex]));
          if (solved) {
            completeGame();
          }
        }
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, sol = []) {
  puzzle = puz;
  solution = sol;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      inp.className = 'sudoku-cell';
      setBoxShadeClass(inp, i, j);
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function readLeaderboard() {
  try {
    const raw = localStorage.getItem(LEADERBOARD_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (error) {
    return [];
  }
}

function writeLeaderboard(entries) {
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(entries));
}

function renderLeaderboard() {
  const listElement = document.getElementById('leaderboard-list');
  if (!listElement) {
    return;
  }

  const entries = readLeaderboard();
  listElement.innerHTML = '';

  if (!entries.length) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'empty';
    emptyItem.innerText = 'No completed games yet.';
    listElement.appendChild(emptyItem);
    return;
  }

  entries.forEach((entry, index) => {
    const item = document.createElement('li');
    const label = `${index + 1}. ${entry.player_name} — ${formatTime(entry.completion_time)} — ${entry.difficulty} — ${entry.hints_used} hint${entry.hints_used === 1 ? '' : 's'}`;
    item.innerText = label;
    listElement.appendChild(item);
  });
}

function submitLeaderboardEntry(playerName) {
  if (!playerName) {
    return false;
  }

  const trimmedName = playerName.trim();
  if (!trimmedName) {
    return false;
  }

  const difficulty = document.getElementById('difficulty').value;
  const leaderboard = readLeaderboard();
  const scoreEntry = {
    game_id: currentGameId,
    player_name: trimmedName,
    completion_time: elapsedSeconds,
    difficulty: difficulty,
    hints_used: hintsUsed,
  };

  const seen = new Map();
  leaderboard.concat(scoreEntry).forEach((entry) => {
    if (!entry || !entry.player_name || typeof entry.completion_time !== 'number' || entry.completion_time < 0) {
      return;
    }

    const normalized = {
      game_id: entry.game_id || `${entry.player_name}-${entry.completion_time}-${entry.difficulty}`,
      player_name: entry.player_name.trim(),
      completion_time: Number(entry.completion_time),
      difficulty: ['easy', 'medium', 'hard'].includes(String(entry.difficulty || '').toLowerCase()) ? String(entry.difficulty).toLowerCase() : 'medium',
      hints_used: Number(entry.hints_used) >= 0 ? Number(entry.hints_used) : 0,
    };

    if (!normalizeLeaderboardEntry(normalized)) {
      return;
    }
    if (seen.has(normalized.game_id)) {
      return;
    }
    seen.set(normalized.game_id, normalized);
  });

  const sorted = Array.from(seen.values()).sort((a, b) => a.completion_time - b.completion_time || a.hints_used - b.hints_used || a.player_name.localeCompare(b.player_name)).slice(0, 10);
  writeLeaderboard(sorted);
  renderLeaderboard();
  return true;
}

function normalizeLeaderboardEntry(entry) {
  if (!entry || !entry.player_name || typeof entry.player_name !== 'string') {
    return null;
  }

  const trimmedName = entry.player_name.trim();
  if (!trimmedName) {
    return null;
  }

  const timeValue = Number(entry.completion_time);
  const hintValue = Number(entry.hints_used);
  const difficulty = String(entry.difficulty || '').toLowerCase();

  if (!Number.isFinite(timeValue) || timeValue < 0 || !Number.isFinite(hintValue) || hintValue < 0 || !['easy', 'medium', 'hard'].includes(difficulty)) {
    return null;
  }

  return {
    game_id: String(entry.game_id || `${trimmedName}-${timeValue}-${difficulty}`),
    player_name: trimmedName,
    completion_time: timeValue,
    difficulty,
    hints_used: Math.floor(hintValue),
  };
}

function completeGame() {
  if (completedGameSubmitted) {
    return;
  }

  const board = getBoardFromInputs();
  const solved = boardIsComplete(board) && board.every((row, rowIndex) => row.every((value, colIndex) => value === solution[rowIndex][colIndex]));
  if (!solved) {
    return;
  }

  completedGameSubmitted = true;
  stopTimer();
  
  const playerName = window.prompt('Enter your name for the leaderboard:', 'Player');
  
  const msg = document.getElementById('message');
  msg.style.color = 'var(--message-success)';
  
  const leaderboardAdded = playerName !== null ? submitLeaderboardEntry(playerName) : false;
  if (leaderboardAdded) {
    msg.innerText = 'Congratulations! You solved it in ' + formatTime(elapsedSeconds) + '! Top 10 updated.';
  } else {
    msg.innerText = 'Congratulations! You solved it in ' + formatTime(elapsedSeconds) + '!';
  }
}

function boardIsComplete(board) {
  return board.every((row) => row.every((value) => value !== 0));
}

async function newGame() {
  currentGameId = `game-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  completedGameSubmitted = false;
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch('/new?difficulty=' + encodeURIComponent(difficulty));
  const data = await res.json();
  hintsUsed = 0;
  document.getElementById('hints-used').innerText = 'Hints used: ' + hintsUsed;
  renderPuzzle(data.puzzle, data.solution || []);
  startTimer();
  document.getElementById('message').innerText = '';
}

async function showHint() {
  const board = getBoardFromInputs();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');

  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }

  const idx = data.row * SIZE + data.col;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const inp = inputs[idx];
  inp.value = data.value;
  inp.disabled = true;
  inp.classList.remove('invalid');
  inp.classList.remove('incorrect');
  inp.classList.add('hinted');
  hintsUsed = data.hints_used;
  document.getElementById('hints-used').innerText = 'Hints used: ' + hintsUsed;
  msg.style.color = 'var(--message-warn)';
  msg.innerText = 'Hint used.';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0] * SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('invalid');
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (data.solved) {
    completeGame();
    return;
  }

  if (incorrect.size > 0) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = 'Some cells are incorrect.';
    return;
  }

  msg.style.color = 'var(--message-warn)';
  msg.innerText = 'Board is incomplete.';
}

// Wire buttons
window.addEventListener('load', () => {
  initializeTheme();
  renderLeaderboard();
  document.getElementById('difficulty').addEventListener('change', newGame);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-solution').addEventListener('click', showHint);
  // initialize
  newGame();
});