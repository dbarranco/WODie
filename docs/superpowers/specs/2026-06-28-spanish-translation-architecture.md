# Spanish Translation Architecture

**Date:** 2026-06-28
**Status:** Approved
**Scope:** Full i18n support for Spanish (ES) with auto-detect + language picker

---

## Overview

Woddy will support Spanish (`es`) alongside English (`en`). The architecture decouples translation from generation:
- **Generate once in English**, then separately in Spanish
- **Serve static Spanish variants** (no runtime translation API calls)
- **Store UI strings** in a centralized translation file
- **Auto-detect browser language** on first load, with manual override via header picker

This maintains Woddy's "zero runtime API calls" principle while enabling full language support.

---

## Directory Structure

```
docs/
├── data/                          # English programs & WODs (default)
│   ├── programs/
│   │   └── back-in-shape-2w.json
│   └── wods/
│       ├── wods-full-body.json
│       ├── wods-upper-body.json
│       ├── wods-lower-body.json
│       ├── wods-strength.json
│       └── wods-cardio.json
│
├── data-es/                       # Spanish programs & WODs (translated)
│   ├── programs/
│   │   └── back-in-shape-2w.json  (all content in Spanish)
│   └── wods/
│       └── ... (same structure as data/)
│
└── i18n/
    ├── en.json                    # English UI strings (reference, optional)
    └── es.json                    # Spanish UI strings + movement names
```

**Key principle:** `data/` and `data-es/` are **structurally identical**. Same filenames, same JSON schema, different language content.

---

## UI String Translation: `docs/i18n/es.json`

Centralized JSON file containing all static UI strings, keyed by semantic ID:

```json
{
  "app.title": "Woddy",
  "app.subtitle": "Programación de CrossFit respaldada por ciencia",
  "onboarding.startProgram": "Comenzar Programa",
  "onboarding.startProgramDesc": "Ciclo de entrenamiento estructurado de 2-4 semanas con carga progresiva",
  "onboarding.dailyWod": "WOD Diario",
  "onboarding.dailyWodDesc": "Entrenamiento drop-in, sin compromiso",
  "programs.chooseProgram": "Elegir un Programa",
  "programs.duration": "Duración del Programa",
  "programs.durationQuestion": "¿Cuántas semanas deseas comprometerte?",
  "programs.frequency": "Frecuencia de Entrenamiento",
  "programs.frequencyQuestion": "¿Cuántos días por semana puedes entrenar?",
  "programs.reset": "↻ Reiniciar",
  "btn.continue": "Continuar",
  "btn.start": "Comenzar Sesión",
  "btn.back": "← Atrás",
  "btn.finish": "TERMINAR",
  "btn.play": "REPRODUCIR",
  "btn.pause": "PAUSA",
  "btn.reset": "REINICIAR",
  "btn.prevBlock": "← BLOQUE ANTERIOR",
  "btn.nextBlock": "SIGUIENTE BLOQUE →",
  "btn.changeCategory": "← Cambiar Categoría",
  "btn.nextWod": "Siguiente WOD",
  "equipment.title": "Equipo Necesario",
  "rationale.title": "🔬 ¿Por Qué Esta Sesión?",
  "timer.nextBlock": "Siguiente:",
  "timer.blockName": "Bloque Activo",
  "timer.roundInfo": "Ronda",
  "wod.selectCategory": "Seleccionar Categoría",
  "wod.fullBody": "Cuerpo Completo",
  "wod.upperBody": "Tren Superior",
  "wod.lowerBody": "Tren Inferior",
  "wod.strength": "Fuerza",
  "wod.cardio": "Cardio",
  "acronyms.AMRAP": "As Many Rounds As Possible",
  "acronyms.EMOM": "Every Minute On the Minute",
  "acronyms.RPE": "Rate of Perceived Exertion",
  "acronyms.C2B": "Chest to Bar",
  "acronyms.1RM": "One-Rep Max",
  "acronyms.RFD": "Rate of Force Development",
  "acronyms.RIR": "Reps In Reserve",
  "acronyms.CARs": "Controlled Articular Rotations",
  "acronyms.ROM": "Range of Motion",
  "acronyms.CNS": "Central Nervous System",
  "movements.backSquat": "Sentadilla Trasera",
  "movements.benchPress": "Press de Banca",
  "movements.deadlift": "Levantamiento de Tierra",
  "movements.pullUp": "Dominada",
  "movements.pushUp": "Flexión",
  "movements.rowingMachine": "Remadora",
  "movements.kettlebellSwing": "Swing de Kettlebell",
  "movements.jumpRope": "Cuerda para Saltar",
  "movements.burpee": "Burpee",
  "movements.boxJump": "Salto a la Caja",
  "movements.wallBall": "Lanzamiento al Muro",
  "movements.medBallClean": "Clean de Balón Medicinal",
  "movements.doubleUnder": "Doble Salto",
  "movements.handstandWalk": "Caminata en Posición Invertida",
  "movements.muscleUp": "Muscle Up",
  "movements.barbell": "Barra",
  "movements.dumbbell": "Mancuerna",
  "movements.kettlebell": "Kettlebell",
  "movements.plates": "Discos",
  "movements.rack": "Rack de Pesas",
  "movements.pullUpBar": "Barra de Dominadas",
  "movements.inchworm": "Inchworm",
  "movements.hipCircles": "Círculos de Cadera",
  "movements.catCow": "Cat-Cow",
  "movements.hipFlexorStretch": "Estiramiento de Flexores de Cadera",
  "movements.worldsGreatestStretch": "Estiramiento Más Genial del Mundo",
  "movements.airSquat": "Sentadilla Aérea",
  "movements.goodMorning": "Good Morning",
  "movements.bandedPullApart": "Abducción con Banda",
  "": "PLACEHOLDER_FOR_ALL_68_MOVEMENTS"
}
```

**Scope:** UI strings + all 68 movement names from `data/movement-library.json`.

---

## Generated Program & WOD Translation

Programs and WODs are **generated in Spanish** via the generator pipeline, not post-translated:

```bash
# Generate English (existing workflow)
python3 scripts/generate.py --type program --name back-in-shape --weeks 2
python3 scripts/generate.py --type wod --count 5 --category full-body

# Generate Spanish (new)
python3 scripts/generate.py --type program --name back-in-shape --weeks 2 --language es
python3 scripts/generate.py --type wod --count 5 --category full-body --language es
```

**Spanish output:**
- Sessions, blocks, movements all written in Spanish
- Rationale text authored in Spanish (not machine-translated)
- Citations and sources preserved
- JSON schema identical to English variant
- Output path: `docs/data-es/programs/` and `docs/data-es/wods/`

**Why generate, not translate?**
- Rationales cite sports science sources — Spanish requires domain expertise, not dictionary lookup
- Movement cues and scaling notes read better when authored naturally in Spanish
- Aligns with "generation is the source of truth" principle
- Easier quality control (validate generated Spanish directly)

---

## Runtime Language Switching

### **Initialization (app.js)**

```javascript
// Global i18n state
const i18n = {
  language: localStorage.getItem('language') || detectBrowserLanguage(),
  strings: {},
};

// Detect browser language on first load
function detectBrowserLanguage() {
  const browserLang = navigator.language.split('-')[0]; // 'es', 'en', etc.
  return ['es', 'en'].includes(browserLang) ? browserLang : 'en';
}

// Load translations at startup
async function initI18n() {
  try {
    i18n.strings = await fetch(`./i18n/${i18n.language}.json`).then(r => r.json());
    applyTranslations();
  } catch (e) {
    console.error('Failed to load translations:', e);
    i18n.language = 'en'; // Fallback
  }
}

// Apply translations to DOM (buttons, labels, etc.)
function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = i18n.strings[key] || key; // Fallback to key if missing
  });
}
```

### **Data Loading (language-aware)**

```javascript
// Construct path based on current language
function getDataPath(type, filename) {
  const dir = i18n.language === 'es' ? 'data-es' : 'data';
  return `./${dir}/${type}/${filename}.json`;
}

// Load a program (automatically uses correct language)
async function loadProgram(programId) {
  const path = getDataPath('programs', programId);
  const data = await fetch(path).then(r => r.json());
  renderProgram(data); // All text already in correct language
}

// Load a WOD
async function loadWod(category) {
  const path = getDataPath('wods', `wods-${category}`);
  const data = await fetch(path).then(r => r.json());
  renderWod(data);
}
```

### **Language Picker (header)**

Add to HTML header:
```html
<select id="language-picker" aria-label="Select language">
  <option value="en">English</option>
  <option value="es">Español</option>
</select>
```

JavaScript:
```javascript
function setupLanguagePicker() {
  const picker = document.getElementById('language-picker');
  picker.value = i18n.language;
  picker.addEventListener('change', (e) => {
    i18n.language = e.target.value;
    localStorage.setItem('language', e.target.value);
    location.reload(); // Full reload to swap all data + UI
  });
}
```

---

## Generator Changes (`scripts/generate.py`)

1. **Add `--language` flag** (default: `en`):
   ```bash
   python3 scripts/generate.py --type program --name back-in-shape --weeks 2 --language es
   ```

2. **Adjust system prompt** based on language:
   - If `--language es`, instruct Claude to write all output in Spanish
   - Keep hard rules, knowledge base, and structure identical

3. **Output path logic**:
   - English: `output/back-in-shape-2w.json` → `docs/data/programs/back-in-shape-2w.json`
   - Spanish: `output-es/back-in-shape-2w.json` → `docs/data-es/programs/back-in-shape-2w.json`

4. **Batch generation script** (`generate-all.sh`):
   - Generate all English variants
   - Generate all Spanish variants
   - Organize outputs by language

---

## HTML Markup Changes

Update static UI strings to use `data-i18n` attributes:

```html
<!-- Before -->
<h1>Woddy</h1>

<!-- After -->
<h1 data-i18n="app.title">Woddy</h1>

<!-- Before -->
<button id="btn-start-program" class="option-card">
  <h3>Start Program</h3>
  <p>Structured 2-4 week training cycle with progressive loading</p>
</button>

<!-- After -->
<button id="btn-start-program" class="option-card">
  <h3 data-i18n="onboarding.startProgram">Start Program</h3>
  <p data-i18n="onboarding.startProgramDesc">Structured 2-4 week training cycle with progressive loading</p>
</button>
```

**Scope:** All UI text nodes get `data-i18n` keys. Movement names and session content come from loaded JSON (already translated).

---

## Implementation Order

1. **Phase 1 — Foundation**
   - Create `docs/i18n/es.json` with all UI strings
   - Add `data-i18n` attributes to HTML
   - Implement `initI18n()` and language detection in app.js
   - Add language picker to header

2. **Phase 2 — Data Generation**
   - Update `scripts/generate.py` to support `--language` flag
   - Generate Spanish programs and WODs
   - Organize output into `docs/data-es/`

3. **Phase 3 — Integration & Testing**
   - Implement `getDataPath()` and update data loaders
   - Test language switching
   - Verify all UI and content renders correctly in both languages

---

## Fallback & Error Handling

- **Missing translation key:** Fall back to English string or display key itself (non-breaking)
- **Missing language data:** Redirect to English (graceful degradation)
- **localStorage persistence:** Language choice survives page refresh
- **Browser language mismatch:** If browser is not `en` or `es`, default to `en`

---

## Performance & Storage

- **Disk space:** ~2× for data files (one English, one Spanish)
  - Current: `~170 KB` for programs + WODs
  - With Spanish: `~340 KB` total (acceptable for PWA)
- **Load time:** Identical to English (static JSON fetch)
- **Translation file:** `i18n/es.json` is ~10 KB (one-time load)

---

## Future Expansion

To add more languages (French, Portuguese, etc.):
1. Create `docs/i18n/fr.json` with French strings
2. Generate French programs/WODs to `docs/data-fr/`
3. Add language option to picker
4. Update `getDataPath()` and `detectBrowserLanguage()` to handle new language

No architectural changes needed.

---

## Validation Checklist

- [ ] All UI strings in `i18n/es.json` are grammatically correct Spanish
- [ ] All 68 movement names are translated
- [ ] Spanish programs/WODs generate without errors
- [ ] `data-es/` structure mirrors `data/` exactly
- [ ] Language picker works (EN ↔ ES switching)
- [ ] Browser auto-detection correctly identifies Spanish speakers
- [ ] localStorage persists language choice
- [ ] Fallback to English works if Spanish file missing
- [ ] All acronyms and technical terms are preserved (not translated)

---

## Git & Deployment

- Commit `docs/i18n/es.json` as human-edited file
- Commit `docs/data-es/` as generated artifacts (gitignore intermediate output/)
- GitHub Pages serves both `data/` and `data-es/` automatically
- No additional deployment steps needed

---

## Notes

- **Acronyms:** CrossFit terminology (AMRAP, EMOM, etc.) is kept in English in both languages (standard practice in Spanish fitness communities)
- **Citations:** Sports science citations are preserved as-is; the rationale text around them is translated
- **Movement library:** `data/movement-library.json` remains English-only (used by generator as reference)
