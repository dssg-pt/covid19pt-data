# COVID-19 Portugal: A Spiral Journey

## An Interactive Data Visualization Experience

This is a surprising and unique visualization of Portugal's COVID-19 pandemic data, presenting the timeline as a beautiful spiral galaxy where data flows through time and space.

## What Makes This Surprising?

Unlike traditional linear charts and graphs, this visualization:

1. **Spiral Timeline** - Data is arranged in a logarithmic spiral (inspired by nature's golden ratio), creating a cosmic journey through the pandemic
2. **Multiple Visualization Modes** - Four completely different ways to experience the same data
3. **Particle Physics** - Flowing particles represent the dynamic nature of the pandemic
4. **Interactive Exploration** - Pan, zoom, and hover to explore every data point
5. **Time Travel** - Animate through the entire pandemic timeline
6. **Multi-layered Data** - Switch between cases, deaths, hospitalizations, ICU, and vaccinations

## Features

### 4 Visualization Modes

1. **Spiral Galaxy** - Data points orbit along a spiral path, with size and glow representing intensity
2. **Particle Flow** - Thousands of particles flow outward from the center, their behavior controlled by the data
3. **Waves** - Rippling concentric circles that pulse with the pandemic's rhythm
4. **Radial Bars** - A circular bar chart showing the data radiating from the center

### Interactive Controls

- **Data Layer Selection** - Choose what metric to visualize:
  - New Cases
  - Deaths
  - Hospitalized Patients
  - ICU Admissions
  - New Vaccinations

- **Animation** - Watch the pandemic unfold over time with adjustable speed
- **Pan & Zoom** - Click and drag to explore, scroll to zoom in/out
- **Hover Tooltips** - Detailed information appears when hovering over data points
- **Real-time Stats** - Current statistics update as you navigate through time

### Visual Design

- **Cosmic Theme** - Deep space gradient background with glowing elements
- **Color-coded Metrics**:
  - 🔴 Red/Pink: Cases and Deaths
  - 💙 Cyan: Hospitalizations and Recovery
  - 💜 Purple: ICU Admissions
  - 💚 Green: Vaccinations
- **Smooth Animations** - 60 FPS canvas-based rendering
- **Glass Morphism UI** - Modern frosted glass control panels

## How to Use

### Method 1: Using the Python Server (Recommended)

```bash
# Run the visualization server
python3 run_visualization.py
```

This will:
- Start a local web server on port 8000
- Automatically open your browser to the visualization
- Properly handle CSV file loading

### Method 2: Using Python's Built-in Server

```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Then open your browser to:
# http://localhost:8000/spiral_viz.html
```

### Method 3: Using Node.js

```bash
# If you have npx installed
npx http-server -p 8000

# Then open your browser to:
# http://localhost:8000/spiral_viz.html
```

## Data Sources

The visualization uses two main data files:

- `data.csv` - Main pandemic data (cases, deaths, hospitalizations, ICU)
- `vacinas.csv` - Vaccination data

Data spans from **March 2, 2020** to **April 5, 2023**, covering the entire pandemic period in Portugal.

## Technical Details

### Technologies
- **Pure JavaScript** - No external dependencies
- **HTML5 Canvas** - High-performance rendering
- **CSS3** - Modern UI with backdrop filters and gradients
- **Vanilla ES6+** - Clean, modern JavaScript

### Performance
- 60 FPS rendering
- Efficient particle system (1000+ particles)
- Smooth zooming and panning
- Optimized data processing

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires ES6+ support
- Works best on desktop (mouse/trackpad for interaction)

## Tips for Exploration

1. **Start with Spiral Mode** - Get an overview of the entire pandemic timeline
2. **Play the Animation** - Watch how the pandemic evolved day by day
3. **Switch to Particle Mode** - See the dynamic flow of data
4. **Try Waves Mode** - Watch the pandemic waves ripple outward
5. **Use Radial Bars** - See the intensity of different periods at a glance
6. **Zoom In** - Examine specific time periods in detail
7. **Hover for Details** - Get exact numbers for any date
8. **Compare Metrics** - Switch between different data layers to see correlations

## What the Data Reveals

Through this visualization, you can observe:

- **Multiple Waves** - Distinct pandemic waves appear as clusters of intense activity
- **Vaccination Impact** - The rise of vaccinations correlating with case reduction
- **Seasonal Patterns** - How cases fluctuated with seasons
- **Healthcare Burden** - ICU and hospitalization patterns during peaks
- **Recovery Periods** - Calm periods between waves
- **The Long Journey** - Over 3 years of data spiraling outward from the center

## Credits

**Data Source**: Portuguese Health Authority (DGS - Direção-Geral da Saúde)
**Visualization**: Created with Claude Code
**Inspiration**: Nature's spirals, cosmic visualizations, and the desire to see data differently

## License

This visualization tool is provided as-is for educational and analytical purposes.

---

**Enjoy your journey through the pandemic spiral!** 🌌
