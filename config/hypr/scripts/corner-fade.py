#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, GtkLayerShell, GLib
import cairo, math, subprocess

DURATION_MS = 500
FPS = 144
STEPS = int(DURATION_MS / (1000 / FPS))

class FadeWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_app_paintable(True)
        visual = self.get_screen().get_rgba_visual()
        if visual:
            self.set_visual(visual)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        for edge in (GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM,
                     GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT):
            GtkLayerShell.set_anchor(self, edge, True)
        GtkLayerShell.set_exclusive_zone(self, -1)

        self.connect("draw", self.on_draw)
        self.step = 0
        self.max_radius = None
        GLib.timeout_add(1000 // FPS, self.tick)

    def on_draw(self, widget, cr):
        w, h = widget.get_allocated_width(), widget.get_allocated_height()
        if self.max_radius is None:
            self.max_radius = math.hypot(w, h)

        progress = self.step / STEPS
        radius = max(self.max_radius * (1 - progress), 0)

        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.rectangle(0, 0, w, h)
        cr.arc(0, 0, radius, 0, 2 * math.pi)
        cr.set_source_rgba(0, 0, 0, 1)
        cr.fill()
        return False

    def tick(self):
        self.step += 1
        self.queue_draw()
        if self.step > STEPS:
            subprocess.run(
            "command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'",
            shell=True
            )
            Gtk.main_quit()
            return False
        return True

win = FadeWindow()
win.show_all()
Gtk.main()
