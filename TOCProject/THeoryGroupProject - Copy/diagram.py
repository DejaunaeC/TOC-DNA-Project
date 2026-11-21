import math

def draw_dfa(canvas, transitions, accepting, start, current):
    R = 28
    W, H = int(canvas["width"]), int(canvas["height"])
    fg = "white"
    canvas.configure(bg="#2b2b2b")
    canvas.delete("all")

    # BFS from start: discovery order, depth, and display names (S0, S1, ...)
    order, depth = [start], {start: 0}
    for s in order:
        for t in transitions[s].values():
            if t not in depth:
                depth[t] = depth[s] + 1
                order.append(t)
    names = {s: f"Q{i}" for i, s in enumerate(order)}

    # Layout: one column per BFS depth, left to right
    cols = {}
    for s in order:
        cols.setdefault(depth[s], []).append(s)
    pos = {}
    for d, group in cols.items():
        x = 50 + d * (W - 100) / (len(cols) - 1)
        for i, s in enumerate(group):
            pos[s] = (x, H * (i + 1) / (len(group) + 1))

    # Merge symbols that share the same edge: (S1 -> S2) labelled "A,T"
    edges = {}
    for s, moves in transitions.items():
        for sym, t in moves.items():
            edges.setdefault((s, t), []).append(sym)

    for (s, t), syms in edges.items():
        label = ",".join(sorted(syms))
        x1, y1 = pos[s]
        x2, y2 = pos[t]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        bend = 28 if (t, s) in edges else 0   # curve if there is a return edge
        cx, cy = mx - dy / dist * bend, my + dx / dist * bend
        a1 = math.atan2(cy - y1, cx - x1)
        a2 = math.atan2(cy - y2, cx - x2)
        sx, sy = x1 + R * math.cos(a1), y1 + R * math.sin(a1)
        ex, ey = x2 + R * math.cos(a2), y2 + R * math.sin(a2)
        canvas.create_line(sx, sy, cx, cy, ex, ey, smooth=True,
                           arrow="last", fill=fg, width=2)
        canvas.create_text((mx + cx) / 2, (my + cy) / 2 - 10, text=label,
                           fill=fg, font=("Arial", 9))

    # States
    for s in order:
        x, y = pos[s]
        active = (s == current)
        canvas.create_oval(x - R, y - R, x + R, y + R,
                           fill="#f1c40f" if active else "#1f6aa5",
                           outline=fg, width=2)
        if s in accepting:  # double circle
            canvas.create_oval(x - R + 5, y - R + 5, x + R - 5, y + R - 5,
                               outline=fg, width=2)
        canvas.create_text(x, y, text=names[s],
                           fill="black" if active else "white",
                           font=("Arial", 10, "bold"))

    # Start arrow
    x, y = pos[start]
    canvas.create_line(x - R - 25, y, x - R, y, arrow="last", fill=fg, width=2)
