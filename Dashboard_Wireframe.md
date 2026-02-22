# Dashboard Design – Wireframe & UX Specification

## Color Theme
| Element | Color | Hex |
|---|---|---|
| Primary (Headers, KPI Cards) | Deep Navy Blue | `#1B2A4A` |
| Secondary (Accents) | Teal | `#00B2A9` |
| Success/Positive | Emerald Green | `#2ECC71` |
| Warning | Amber | `#F39C12` |
| Danger/Negative | Crimson | `#E74C3C` |
| Background | Light Gray | `#F5F6FA` |
| Card Background | White | `#FFFFFF` |
| Text Primary | Dark Charcoal | `#2C3E50` |
| Text Secondary | Slate | `#7F8C8D` |

## Global Slicers (Applied to All Pages)
| Slicer | Type | Position |
|---|---|---|
| Academic Year | Dropdown | Top-left |
| Class | Dropdown multi-select | Top bar |
| Section | Buttons (A / B / All) | Top bar |
| Month | Dropdown | Top bar |
| Performance Category | Dropdown | Top bar |

## Drill-Through Design
- **Student Detail Page**: Right-click any student → drill-through to individual student profile showing all metrics
- **Class Detail**: Click any class in bar chart → drill-through to class breakdown
- **Subject Detail**: Click any subject → drill-through to subject-level month-by-month analysis

---

## PAGE 1: Executive Overview

### Layout Grid (12-column, 3 rows)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ROW 1: KPI CARDS (6 cards, equal width)                               │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │Total     │ │Revenue   │ │Overall   │ │Attendance│ │Pass %    │ │Fee       │ │
│ │Students  │ │Collected │ │Academic %│ │%         │ │          │ │Collection│ │
│ │  611     │ │₨ 12.5M   │ │ 62.3%    │ │ 79.4%    │ │ 94.2%    │ │ 72.1%    │ │
│ │ ↑ vs LY  │ │ ↑ 8%     │ │ ↑ 2.1%   │ │ ↓ 0.5%   │ │ ↑ 1.3%   │ │ ↓ 3.2%   │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 2 (Left 8 cols): Trend Line   │ ROW 2 (Right 4 cols): Donut     │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Monthly Academic Trend           │ │  Paid vs Unpaid (Donut)      │  │
│ │  LINE CHART                       │ │  DONUT CHART                 │  │
│ │  X: Month (Academic Order)        │ │  Green = Paid                │  │
│ │  Y: Avg Percentage                │ │  Red = Unpaid                │  │
│ │  Legend: Section A / B            │ │  Center: Collection %        │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 3 (Left 6 cols): Bar Chart    │ ROW 3 (Right 6 cols): Table     │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Class-wise Student Count         │ │  Quick Stats Table            │  │
│ │  STACKED BAR CHART                │ │  MATRIX                      │  │
│ │  X: Class 1-10                    │ │  Rows: Class                 │  │
│ │  Y: Count                         │ │  Values: Students, Avg%,     │  │
│ │  Legend: Male / Female            │ │    Attendance, Fee Status    │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Visual Types
| Visual | Type | Interaction |
|---|---|---|
| KPI Cards | Card with conditional formatting + sparkline | Hover for detail |
| Monthly Trend | Line Chart (dual axis possible) | Cross-filter |
| Paid vs Unpaid | Donut Chart | Click to filter |
| Class Count | Stacked Bar | Drill-through to class |
| Quick Stats | Matrix | Sortable columns |

---

## PAGE 2: Academic Analytics

### Layout Grid

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ROW 1 (Full width): Subject Heatmap                                    │
│ ┌───────────────────────────────────────────────────────────────────────┐ │
│ │  MATRIX HEATMAP                                                      │ │
│ │  Rows: Subject (8)                                                   │ │
│ │  Columns: Month (10)                                                 │ │
│ │  Values: Avg Percentage (conditional color scale: Red→Yellow→Green)  │ │
│ │  Cell colors: <50% Red, 50-70% Yellow, >70% Green                   │ │
│ └───────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 2 (Left 6 cols): Class Compare │ ROW 2 (Right 6 cols): Top/Bottom │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Class Comparison                 │ │ Top 5 & Bottom 5 Students   │  │
│ │  CLUSTERED BAR CHART              │ │ TABLE (two colored sections) │  │
│ │  X: Class 1-10                    │ │ Top 5: Green rows            │  │
│ │  Y: Avg Percentage                │ │ Bottom 5: Red rows           │  │
│ │  Legend: Section A / B            │ │ Cols: Name, Class, Avg %     │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 3 (Left 6): Monthly Trend      │ ROW 3 (Right 6): Distribution  │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Month-over-Month Score Trend     │ │  Performance Distribution    │  │
│ │  AREA CHART                       │ │  STACKED COLUMN / PIE        │  │
│ │  X: Month                         │ │  High / Average / Low        │  │
│ │  Y: Avg Score                     │ │  15% / 60% / 25%            │  │
│ │  Color: Gradient fill             │ │  Color: Green/Yellow/Red     │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Visual Types
| Visual | Type | Interaction |
|---|---|---|
| Subject Heatmap | Matrix with background color rules | Cross-filter on click |
| Class Comparison | Clustered Bar Chart | Drill-through to class |
| Top/Bottom Students | Table with conditional row colors | Drill-through to student |
| Monthly Trend | Area Chart | Tooltip with details |
| Performance Distribution | Stacked Column or Pie | Filter on segment click |

---

## PAGE 3: Attendance Insights

### Layout Grid

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ROW 1: KPI Cards (4 cards)                                            │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│ │ Avg Attend % │ │ Risk Students│ │ Excellent %  │ │ Critical %   │   │
│ │   79.4%      │ │     128      │ │    22.3%     │ │     5.7%     │   │
│ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 2 (Left 8 cols): Trend Line   │ ROW 2 (Right 4 cols): Category   │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Attendance Trend by Month        │ │  Attendance Category Split   │  │
│ │  LINE CHART with markers          │ │  DONUT CHART                 │  │
│ │  X: Month                         │ │  Excellent / Good /          │  │
│ │  Y: Avg Attendance %              │ │  Satisfactory / Low /        │  │
│ │  Legend: Section A / B            │ │  Critical                    │  │
│ │  Reference line at 75% (red)      │ │                              │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 3 (Left 6): Scatter Plot      │ ROW 3 (Right 6): Risk Table    │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Attendance vs Performance         │ │  At-Risk Students List       │  │
│ │  SCATTER PLOT                      │ │  TABLE                       │  │
│ │  X: Avg Attendance %               │ │  Cols: Name, Class,          │  │
│ │  Y: Avg Academic %                 │ │    Avg Att%, Status,         │  │
│ │  Color: Performance Category       │ │    Trend Arrow               │  │
│ │  Size: Fixed                       │ │  Filter: Attendance < 75%    │  │
│ │  Trend line overlay                │ │  Sorted: Ascending           │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PAGE 4: Financial Dashboard

### Layout Grid

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ROW 1: KPI Cards (5 cards)                                            │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │
│ │ Expected   │ │ Collected  │ │Outstanding │ │Collection %│ │Defaulters │ │
│ │₨ 21.3M     │ │₨ 15.4M     │ │₨ 5.9M      │ │ 72.1%      │ │ 184       │ │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 2 (Left 8 cols): Revenue Trend │ ROW 2 (Right 4 cols): Status    │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Monthly Revenue Trend            │ │  Payment Status Mix          │  │
│ │  COMBO CHART (Bar + Line)         │ │  STACKED BAR                 │  │
│ │  Bars: Expected vs Collected      │ │  By Class: Paid vs Unpaid    │  │
│ │  Line: Collection %               │ │  Color: Green / Red          │  │
│ │  X: Month                         │ │                              │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│  ROW 3 (Left 6): Class Revenue     │ ROW 3 (Right 6): Scholarship   │
│ ┌───────────────────────────────────┐ ┌──────────────────────────────┐  │
│ │  Revenue by Class                 │ │  Scholarship Impact          │  │
│ │  HORIZONTAL BAR CHART             │ │  WATERFALL CHART             │  │
│ │  Y: Class 1-10                    │ │  Categories: Total Expected, │  │
│ │  X: Amount (PKR)                  │ │    Scholarship Discount,     │  │
│ │  Color: Gradient by amount        │ │    Final Collected           │  │
│ └───────────────────────────────────┘ └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## UX Suggestions

1. **Navigation**: Use Power BI page navigation buttons with icons (🏠 Overview, 📊 Academic, 📋 Attendance, 💰 Finance)
2. **Tooltips**: Custom tooltip pages showing student-level detail on hover
3. **Bookmarks**: Create bookmarks for "School Overview", "At-Risk Students", "Fee Collection Focus"
4. **Mobile Layout**: Create separate mobile-optimized layouts for each page
5. **Conditional Formatting**: 
   - KPI cards: Green arrow ↑ for positive, Red arrow ↓ for negative trends
   - Tables: Data bars for percentage columns
   - Heatmap: 3-color gradient scale (Red-Yellow-Green)
6. **Themes**: Import a custom JSON theme file matching the color palette above
7. **Bookmarks for Drill-Through Reset**: Add a "Back" button on all drill-through pages
8. **Dynamic Titles**: Use DAX measures for dynamic page titles showing selected filters
