# ARCHITECT_TODO — cts-mastery-quiz-native
_Head Architect review 2026-07-02. Full context: `Code/_ARCHITECT_REVIEW_2026-07-02/`._
_Worker rules: NEVER delete source code (only venv/node_modules/target/.build/__pycache__/dist and compiled artifacts). Move whole projects to `Code/Archived_Projects/<name>/` with WHY_ARCHIVED.md. Before moving a folder, run: grep -rl "cts-mastery-quiz-native" ~/Library/LaunchAgents/ "$HOME/Library/Application Support/BatesAI/" — if anything matches, STOP and report. Secrets (*.p8, *.p12, .env, keys) go to ~/Library/Application Support/BatesAI/keys/ chmod 600. Do ONE step at a time; verify; report._

**Verdict:** CONSOLIDATE into CTS_Quiz/
**What this is:** React Native/Expo scaffold of the CTS certification quiz.

## Steps
1. Create `Code/CTS_Quiz/` with subfolders web/, native/, tools/.
2. Move this folder → CTS_Quiz/native/; `cts_quiz_pwa_assets` → CTS_Quiz/web/; `Technology/CTS_Quiz.html` → CTS_Quiz/web/; root `generate_questions.py`+`fix_quiz.py` and SHIFITING_TILES_FIX.md → CTS_Quiz/tools/.
3. Open the HTML quiz in a browser and verify it still works.
