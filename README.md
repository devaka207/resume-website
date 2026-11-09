# Akshay Hegde – Personal Resume & Portfolio Website

> **Web Development Mid-Term Project (`WD_MTProject`)**  
> An executive-grade, fully responsive personal resume and portfolio website engineered using semantic HTML5, modern CSS3 styling, responsive Flexbox and Grid layouts, and custom design systems.

---

## 🔗 Project Links

- **Live Website Link (GitHub Pages):** [https://devaka207.github.io/resume-website/](https://devaka207.github.io/resume-website/)
- **GitHub Repository Link:** [https://github.com/devaka207/resume-website](https://github.com/devaka207/resume-website)
- **LinkedIn Profile:** [https://www.linkedin.com/in/akshayshridhar/](https://www.linkedin.com/in/akshayshridhar/)

---

## 🚀 Key Improvements & CSS Concepts Applied

1. **Typography & Font Strategy:**
   - Integrated Google Fonts: **Plus Jakarta Sans** (headings) and **Inter** (body copy).
   - Applied fluid typography scaling via `clamp()`, balanced line-heights (`1.6` for body, `1.25` for headers), and proportional letter spacing.

2. **Color Palette & CSS Custom Properties (`:root`):**
   - Established an **Executive Tech** palette with WCAG AA compliance:
     - Primary Dark: `#0f172a` (Slate Charcoal)
     - Brand Blue: `#2563eb` (Royal Sapphire)
     - Accent Sky: `#0ea5e9` (Vibrant Cyan)
     - Clean Surfaces: `#ffffff` & `#f8fafc`
     - Borders: `#e2e8f0`

3. **Positioning & Navigation Architecture:**
   - Top sticky navigation bar (`position: sticky; top: 0; z-index: 1000;`).
   - Frosted-glass backdrop effect (`backdrop-filter: blur(12px);`).
   - Animated link underlines on hover using `::after` pseudo-elements.
   - Responsive mobile navigation drawer with a hamburger button.

4. **Display Modes (Flexbox & CSS Grid):**
   - **Flexbox:** Navigation bar alignment, hero action button cluster, badge pills, metric counters, and timeline entries.
   - **CSS Grid:** Responsive multi-column layouts using `repeat(auto-fit, minmax(...))` for About feature cards, Flagship Ventures, and Skills metrics.

5. **CSS Selectors Variety:**
   - Universal box-sizing reset (`*, *::before, *::after { box-sizing: border-box; }`).
   - Component classes (`.card`, `.btn`, `.btn-primary`, `.badge-pill`, `.grid-2`, `.grid-3`).
   - ID selectors for smooth anchor scrolling (`#hero`, `#about`, `#ventures`, `#experience`, `#skills`, `#education`, `#contact`).
   - Attribute selectors (`input[type="email"]`, `a[target="_blank"]`) and pseudo-states (`:hover`, `:focus`, `:active`).

---

## 📁 File Structure

```text
resume-website/
├── index.html               # Semantic HTML5 resume website
├── styles.css               # Complete modern CSS stylesheet (responsive, grid, flexbox)
├── script.js                # Light interactive script (mobile menu & scroll spy)
├── submission_report.html   # Browser-printable 2-page submission document
├── generate_pdf.py          # Automated zero-dependency PDF generator
├── 25129999_WD_MTProject.pdf# Generated submission PDF (1–2 pages)
└── README.md                # Documentation and hosting guide
```

---

## 🌐 How to Host on GitHub Pages

1. **Create a new repository on GitHub:**
   - Go to [https://github.com/new](https://github.com/new)
   - Repository name: `resume-website`
   - Set to **Public**

2. **Push the project from your terminal:**
   ```bash
   cd /Users/akshay/.gemini/antigravity/scratch/resume-website
   git remote add origin https://github.com/devaka207/resume-website.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - In your repository, go to **Settings** > **Pages**
   - Under **Build and deployment** > **Source**, select `Deploy from a branch`
   - Select branch: `main`, folder: `/ (root)`
   - Click **Save**
   - Your site will be live at: `https://devaka207.github.io/resume-website/`

---

## 📄 Generating Your Final Submission PDF

To generate the submission PDF with your exact Roll Number:

```bash
cd /Users/akshay/.gemini/antigravity/scratch/resume-website
python3 generate_pdf.py <YOUR_ROLL_NO>
```

*Example:*
```bash
python3 generate_pdf.py 25129999
```
This will create `25129999_WD_MTProject.pdf` (strictly 2 pages, containing the live link, repo link, write-up of CSS improvements, and section-by-section design rationale).

Alternatively, you can open `submission_report.html` in your desktop browser and click **Print / Save as PDF**.
