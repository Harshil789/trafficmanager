# Design Guidelines: Smart Traffic Monitoring System (Fog + Edge Computing)

## Design Approach: Material Design System
**Rationale:** This is a data-heavy, educational monitoring application requiring clear information hierarchy and real-time data visualization. Material Design excels at creating structured, information-dense interfaces with strong visual feedback.

## Typography System

**Font Family:** Roboto (via Google Fonts CDN)
- Primary: Roboto Regular (400) for body text
- Emphasis: Roboto Medium (500) for labels and section headers
- Headings: Roboto Bold (700) for main titles

**Type Scale:**
- Page Title: text-3xl (30px)
- Section Headers: text-xl (20px)
- Data Labels: text-sm (14px) uppercase tracking-wide
- Body/Logs: text-base (16px) monospace for console output
- Timestamps: text-xs (12px)

## Layout System

**Spacing Primitives:** Use Tailwind units of 2, 4, 6, and 8
- Component padding: p-4, p-6
- Section gaps: gap-4, gap-6
- Container margins: m-4, m-8
- Card spacing: space-y-4

**Grid Structure:**
- Main container: max-w-7xl mx-auto px-4
- Three-column layout for layer visualization (Edge | Fog | Cloud)
- Responsive: Stack to single column on mobile (md:grid-cols-3)

## Component Library

### 1. Dashboard Layout
- Top navigation bar: Full-width sticky header with project title and status indicator
- Main content area: Three-column grid showing architectural layers
- Console log section: Full-width panel at bottom (min-height: 300px)

### 2. Layer Cards (Edge, Fog, Cloud)
Each computational layer represented as elevated card:
- Border treatment with subtle elevation
- Header with layer icon and name
- Data display area showing current metrics
- Status indicator (active/idle)
- Dimensions: Equal width columns, min-height: 400px

### 3. Control Panel
Central trigger section above layer visualization:
- Prominent action button: "Send Traffic Data"
- Secondary button: "Clear Logs"
- Current system status text
- Button sizing: px-8 py-3 for primary action

### 4. Data Flow Visualization
Between layer cards, show connection indicators:
- Animated arrows/lines showing data movement direction
- Latency badges displaying millisecond values
- Visual pulse when data transfers occur

### 5. Metrics Display
Within each layer card:
- Vehicle Count: Large numeric display
- Congestion Level: Badge component (Low/Medium/High)
- Processing Time: Small timestamp
- Use dl/dt/dd structure for key-value pairs

### 6. Console Log Panel
Bottom section with terminal-style output:
- Monospace font (font-mono)
- Dark container for contrast
- Auto-scroll to latest entry
- Timestamp prefix for each log line
- Syntax highlighting: Edge (blue accent), Fog (orange accent), Cloud (green accent)
- Max height with overflow scroll

### 7. Info Cards (Educational Section)
Below main dashboard, accordion or expandable cards:
- "What is Edge Computing?"
- "What is Fog Computing?"
- "How This System Works"
- Each card: px-6 py-4, expandable content

## Navigation & Header

**Top Bar Structure:**
- Left: Project title "Smart Traffic Monitor" with traffic icon
- Center: Real-time system status badge
- Right: Info toggle button
- Height: h-16, sticky positioning

## Interaction Patterns

**Primary Actions:**
- Button states: Clear default, subtle hover elevation, active press feedback
- Data updates: Smooth transitions (transition-all duration-300)
- Log entries: Fade-in animation for new items

**Feedback Indicators:**
- Loading spinner during data processing
- Success/error toast notifications for actions
- Pulsing dot for active data transmission

## Responsive Behavior

**Desktop (lg+):**
- Three-column layer layout
- Side-by-side metrics
- Full-width console at bottom

**Tablet (md):**
- Two-column with Cloud below
- Adjusted card padding (p-4)

**Mobile (base):**
- Single column stack: Edge → Fog → Cloud
- Full-width control buttons
- Reduced spacing (gap-3, p-3)

## Images

**Icons Only:** This functional dashboard doesn't require hero images. Use:
- Traffic light icon for project branding (header)
- Server/node icons for each computational layer
- Arrow/connection icons for data flow
- Chart/analytics icon for cloud layer

All icons from Material Icons CDN, sized at 24px-48px depending on context.

## Accessibility

- Clear focus indicators on interactive elements
- Semantic HTML for log structure (time, data, level)
- ARIA labels for layer status indicators
- Keyboard navigation for trigger buttons
- High contrast text in console panel