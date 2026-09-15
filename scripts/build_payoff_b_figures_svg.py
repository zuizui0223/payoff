from __future__ import annotations

from pathlib import Path

from src.anti_phase_temporal import dimensionless_premium, exact_optimal_dimensionless_migration

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "theoretical_ecology" / "generated" / "figures"


def _polyline(points: list[tuple[float, float]], *, cls: str = "curve") -> str:
    xy = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{xy}" class="{cls}" fill="none"/>'


def fig1() -> str:
    width, height = 1200, 760
    x0, y0, pw, ph = 120, 120, 980, 500
    u_max = 6.0
    vs = [0.2, 1.0, 3.0]
    samples = 181
    raw: dict[float, list[tuple[float, float]]] = {}
    max_f = 0.0
    for v in vs:
        vals = []
        for i in range(samples):
            u = u_max * i / (samples - 1)
            f = dimensionless_premium(u, v)
            vals.append((u, f))
            max_f = max(max_f, f)
        raw[v] = vals
    max_f *= 1.08

    def sx(u: float) -> float:
        return x0 + pw * u / u_max

    def sy(f: float) -> float:
        return y0 + ph - ph * f / max_f

    dash = ["", "dash", "dot"]
    curves = []
    markers = []
    labels = []
    for j, v in enumerate(vs):
        pts = [(sx(u), sy(f)) for u, f in raw[v]]
        curves.append(_polyline(pts, cls=f"curve {dash[j]}".strip()))
        us = exact_optimal_dimensionless_migration(v)
        fs = dimensionless_premium(us, v)
        markers.append(f'<circle cx="{sx(us):.2f}" cy="{sy(fs):.2f}" r="7" class="peak"/>')
        labels.append(f'<text x="{sx(us)+12:.2f}" y="{sy(fs)-8:.2f}" class="small">v={v:g}, u*={us:.2f}</text>')

    ticks = []
    for u in range(0, 7):
        x = sx(float(u))
        ticks.append(f'<line x1="{x:.2f}" y1="{y0+ph}" x2="{x:.2f}" y2="{y0+ph+8}" class="axis"/>')
        ticks.append(f'<text x="{x:.2f}" y="{y0+ph+35}" text-anchor="middle" class="tick">{u}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.title{{font:700 34px sans-serif;fill:#111}} .txt{{font:23px sans-serif;fill:#111}} .small{{font:18px sans-serif;fill:#111}}
.tick{{font:18px sans-serif;fill:#111}} .axis{{stroke:#111;stroke-width:2}} .curve{{stroke:#111;stroke-width:4}}
.dash{{stroke-dasharray:14 9}} .dot{{stroke-dasharray:4 8}} .peak{{fill:white;stroke:#111;stroke-width:3}}
</style>
<text x="60" y="56" class="title">Figure 1. Every nonzero contrast has one finite migration optimum</text>
<text x="60" y="88" class="txt">Exact temporal premium F(u,v) for three dimensionless contrasts.</text>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+ph}" class="axis"/>
<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" class="axis"/>
{''.join(ticks)}
{''.join(curves)}
{''.join(markers)}
{''.join(labels)}
<text x="{x0+pw/2}" y="{y0+ph+78}" text-anchor="middle" class="txt">dimensionless migration u = mτ</text>
<text x="34" y="{y0+ph/2}" transform="rotate(-90 34 {y0+ph/2})" text-anchor="middle" class="txt">temporal premium F = τP</text>
<text x="{x0+650}" y="{y0+70}" class="small">solid: v=0.2   dashed: v=1   dotted: v=3</text>
</svg>'''


def fig2() -> str:
    width, height = 1200, 760
    x0, y0, pw, ph = 120, 120, 980, 500
    import math

    log_min, log_max = -2.0, 1.5
    samples = 120
    data = []
    for i in range(samples):
        lv = log_min + (log_max - log_min) * i / (samples - 1)
        v = 10.0**lv
        data.append((lv, exact_optimal_dimensionless_migration(v)))
    y_min, y_max = 0.95, 1.67

    def sx(lv: float) -> float:
        return x0 + pw * (lv - log_min) / (log_max - log_min)

    def sy(u: float) -> float:
        return y0 + ph - ph * (u - y_min) / (y_max - y_min)

    exact = _polyline([(sx(lv), sy(u)) for lv, u in data], cls="curve")
    strong = []
    for i in range(samples):
        lv = log_min + (log_max - log_min) * i / (samples - 1)
        v = 10.0**lv
        approx = 1.0 + 1.0 / v
        if approx <= y_max:
            strong.append((sx(lv), sy(approx)))
    strong_line = _polyline(strong, cls="asym") if strong else ""
    weak_y = sy(1.60611529880277)
    one_y = sy(1.0)

    xticks = []
    for lv, lab in [(-2,"0.01"),(-1,"0.1"),(0,"1"),(1,"10")]:
        x = sx(lv)
        xticks.append(f'<line x1="{x:.2f}" y1="{y0+ph}" x2="{x:.2f}" y2="{y0+ph+8}" class="axis"/>')
        xticks.append(f'<text x="{x:.2f}" y="{y0+ph+35}" text-anchor="middle" class="tick">{lab}</text>')
    yticks = []
    for u in [1.0,1.2,1.4,1.6]:
        y = sy(u)
        yticks.append(f'<line x1="{x0-8}" y1="{y:.2f}" x2="{x0}" y2="{y:.2f}" class="axis"/>')
        yticks.append(f'<text x="{x0-16}" y="{y+6:.2f}" text-anchor="end" class="tick">{u:.1f}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.title{{font:700 34px sans-serif;fill:#111}} .txt{{font:23px sans-serif;fill:#111}} .small{{font:18px sans-serif;fill:#111}}
.tick{{font:18px sans-serif;fill:#111}} .axis{{stroke:#111;stroke-width:2}} .curve{{stroke:#111;stroke-width:4;fill:none}}
.asym{{stroke:#666;stroke-width:3;stroke-dasharray:12 8;fill:none}} .ref{{stroke:#777;stroke-width:2;stroke-dasharray:5 7}}
</style>
<text x="60" y="56" class="title">Figure 2. One scaling curve links weak and strong contrast</text>
<text x="60" y="88" class="txt">The exact optimum u*(v) stays on the seasonal timescale.</text>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+ph}" class="axis"/>
<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" class="axis"/>
{''.join(xticks)}{''.join(yticks)}
<line x1="{x0}" y1="{weak_y:.2f}" x2="{x0+pw}" y2="{weak_y:.2f}" class="ref"/>
<line x1="{x0}" y1="{one_y:.2f}" x2="{x0+pw}" y2="{one_y:.2f}" class="ref"/>
{exact}{strong_line}
<text x="{x0+28}" y="{weak_y-10:.2f}" class="small">weak-contrast limit 1.606115…</text>
<text x="{x0+650}" y="{one_y-10:.2f}" class="small">strong-contrast limit 1</text>
<text x="{x0+690}" y="{y0+115}" class="small">solid: exact u*(v)</text>
<text x="{x0+690}" y="{y0+145}" class="small">dashed: 1 + 1/v asymptote</text>
<text x="{x0+pw/2}" y="{y0+ph+78}" text-anchor="middle" class="txt">dimensionless contrast v = |x|τ (log scale)</text>
<text x="34" y="{y0+ph/2}" transform="rotate(-90 34 {y0+ph/2})" text-anchor="middle" class="txt">optimal u* = m*τ</text>
</svg>'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "FIG1_UNIQUE_OPTIMUM.svg").write_text(fig1(), encoding="utf-8")
    (OUT / "FIG2_SCALING_CURVE.svg").write_text(fig2(), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
