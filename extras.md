### ✅ Feature Roadmap & Enhancements

---

#### 📦 **V2 – Functional Enhancements**

1. **Player Photograph Integration**
   Extract player image from player profile URL and store it inside the `player_info` table.

2. **Dynamic Variable Assignment**
   Replace repetitive if/else assignments using Python's built-in `getattr()` and `setattr()`.

3. **Grounds Metadata Enrichment**

   * Add ground images, location, and home country.
   * Parse ground names from matches.
   * Match with an enriched external dataset.
     *(Initial logic is in `check.ipynb` — needs optimization and modularization.)*

4. **Role-Based Column Pruning**
   Remove irrelevant columns depending on player role:

   * Batters → drop bowling/wicketkeeping columns
   * Bowlers → drop detailed batting fields

---

#### 🧱 **V3 – Structural & Codebase Refinement**

1. **Full Documentation and Linting**
   Add complete docstrings, type hints, and linting across all modules (PEP8-compliant).

2. **Development Containers**
   Create separate Docker containers or venvs per module (scraper, transformer, loader, aggregator).

3. **Class Inheritance Refactoring**
   Streamline OOP structure to allow shared utilities and class extensions across core modules.

4. **Optimize Loader with Class-Level `data_type`**
   Avoid multiple instances of the Loader class by making `data_type` a class-level or optional param.

---

#### 📘 **V4 – Scalability & Documentation**

1. **Full Parameterization**
   Build config-based execution (e.g., YAML or CLI input) for player name, bucket name, etc.

2. **Create a GitHub Wiki**
   Set up a detailed wiki or MkDocs site for developer-level documentation.

3. **Custom Exception Handling**
   Build a custom `CricketStatsError` base class and modular exception hierarchy for better error traceability.
