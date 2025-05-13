import pygame
import tkinter as tk
from tkinter import ttk

materials = {
    "羽毛" : {
        "mass" : 0.01,
        "area" : 0.05,
        "Cd" : 1.2,
    },
    "石" : {
        "mass" : 0.5,
        "area" : 0.01,
        "Cd" : 0.47,
    },
    "木" : {
        "mass" : 0.2,
        "area" : 0.03,
        "Cd" : 0.8,
    },
    "鉄球" : {
        "mass" : 1.0,
        "area" : 0.001,
        "Cd" : 0.47,
    },
    "質点" : {
        "mass" : 0.1,
        "area" : 0.0,
        "Cd" : 0.0,
    },
    "カスタム" : None,
}

LABELS_JP = {
    "mass": "質量 (kg)",
    "area": "断面積 (m²)",
    "Cd": "抗力係数(kg/m²)"
}

def create_material_input(frame, label_text):
    var  = tk.StringVar(value="羽毛")
    custom_name_var = tk.StringVar(value="カスタム")
    custom_vars = {
        "mass": tk.DoubleVar(value=0.01),
        "area": tk.DoubleVar(value=0.05),
        "Cd": tk.DoubleVar(value=1.2),
    }

    def update_state(*_):
        material = var.get()
        if material == "カスタム":
            custom_name_var.set("")
            name_entry.config(state=tk.NORMAL)
            custom_vars["mass"].set(0.1)
            custom_vars["area"].set(0.0)
            custom_vars["Cd"].set(0.0)
            state_map = {
                "mass": tk.NORMAL,
                "area": tk.NORMAL,
                "Cd": tk.NORMAL,
            }
        elif material == "質点":
            name_entry.config(state="readonly")
            custom_name_var.set("質点")
            custom_vars["mass"].set(0.1)
            custom_vars["area"].set(0.0)
            custom_vars["Cd"].set(0.0)
            state_map = {
                "mass": tk.NORMAL,
                "area": tk.DISABLED,
                "Cd": tk.DISABLED,
            }
        else:
            name_entry.config(state="readonly")
            m = materials[material]
            custom_name_var.set(material)
            custom_vars["mass"].set(m["mass"])
            custom_vars["area"].set(m["area"])
            custom_vars["Cd"].set(m["Cd"])
            state_map = {
                "mass": "readonly",
                "area": "readonly",
                "Cd": "readonly",
            }

        for key, entry in entries.items():
            entry.config(state=state_map[key])

    frame = ttk.LabelFrame(frame, text=label_text)
    frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame, text="素材:").grid(row=0, column=0, padx=5, pady=5)
    menu = ttk.OptionMenu(frame, var, var.get(), *materials.keys(), command=update_state)
    menu.grid(row=0, column=1)

    ttk.Label(frame, text="名前:").grid(row=1, column=0)
    name_entry = ttk.Entry(frame, textvariable=custom_name_var, width=10)
    name_entry.grid(row=1, column=1)
    
    entries = {}
    for i, key in enumerate(["mass","area", "Cd"]):
        ttk.Label(frame, text=LABELS_JP[key]).grid(row=i+2, column=0)
        entry = ttk.Entry(frame, textvariable=custom_vars[key], width=10)
        entry.grid(row=i+2, column=1)
        entries[key] = entry

    update_state()
    return var, custom_vars, custom_name_var

def start_pygame_simulation(m1, m2, g, h):
    simulation_done = False
    
    rho = 1.2
    dt = 0.01

    pygame.init()
    W, H_px = 800, 600
    margin = 100
    usable_height_px = H_px - margin
    base_scale = 100
    scale = usable_height_px / h
    scale_factor = min(max(base_scale / scale * 0.1, 0.5), 2.0)
    adjusted_dt = min(dt * scale_factor, 0.05)
    ideal_ticks = 10
    tick_interval = max(1, round(h / ideal_ticks))

    y1 = y2 = h
    v1 = v2 = 0.0
    t = 0.0

    landed1 = landed2 = False
    landed1_time = landed2_time = 0.0

    screen = pygame.display.set_mode((W, H_px))
    pygame.display.set_caption("落下実験")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("meiryo", 18)

    running = True
    while running:
        fps = int(60 * scale_factor)
        clock.tick(min(max(fps, 15), 120))
        t += adjusted_dt
        screen.fill((255, 255, 255))

        for h_m in range(0, int(h) + 1, tick_interval):
            y_pos = int(50 + (h - h_m) * scale)
            pygame.draw.line(screen, (200, 200, 200), (600, y_pos), (790, y_pos), 1)
            text = font.render(f"{h_m} m", True, (100, 100, 100))
            screen.blit(text, (610, y_pos - 10))

        if not landed1:
            a1 = - g + (0.5 * m1["Cd"] * rho * m1["area"] * v1**2 / m1["mass"])
            v1 += a1 * adjusted_dt
            y1 += v1 * adjusted_dt
            if y1 <= 0:
                y1 = 0
                landed1 = True
                landed1_time = t

        if not landed2:
            a2 = - g + (0.5 * m2["Cd"] * rho * m2["area"] * v2**2 / m2["mass"])
            v2 += a2 * adjusted_dt
            y2 += v2 * adjusted_dt
            if y2 <= 0:
                y2 = 0
                landed2 = True
                landed2_time = t

        py1 = int(50 + (h - y1) * scale)
        py2 = int(50 + (h - y2) * scale)

        pygame.draw.circle(screen, (0, 0, 255), (200, py1), 10)
        pygame.draw.circle(screen, (255, 0, 0), (400, py2), 10)

        screen.blit(font.render(f"時間: {t:.2f} 秒", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"{m1['name']}: 速度{-v1:.2f} m/s", True, (0, 0, 0)), (10, 40))
        screen.blit(font.render(f"着地時間: {landed1_time:.2f} 秒", True, (0, 0, 0)), (10, 70))
        screen.blit(font.render(f"{m2['name']}: 速度{-v2:.2f} m/s", True, (0, 0, 0)), (10, 100))
        screen.blit(font.render(f"着地時間: {landed2_time:.2f} 秒", True, (0, 0, 0)), (10, 130))        

        if simulation_done:
            screen.blit(font.render("終了(Escキーで閉じる)", True, (100, 0, 0)), (10, 560))

        pygame.display.flip()

        if landed1 and landed2:
            simulation_done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()

def run_simulation():
    def get_values(var, custom, custom_name_var):
        material = var.get()
        if material == "カスタム":
            return {
                "name": custom_name1.get() if var is material1_var else custom_name2.get(),
                "mass": custom["mass"].get(),
                "area": custom["area"].get(),
                "Cd": custom["Cd"].get()
            }
        else:
            data = materials[material]
            return {
                "name": material,
                "mass": data["mass"],
                "area": data["area"],
                "Cd": data["Cd"]
            }


    m1 = get_values(material1_var, custom1, custom_name1)
    m2 = get_values(material2_var, custom2, custom_name2)
    h = height_var.get()
    g = gravity_var.get()

    print("--- Simulation Parameters ---")
    print("Material 1:", m1)
    print("Material 2:", m2)
    print("Initial height:", h)
    print("Gravity:", g)

    start_pygame_simulation(m1, m2, g, h)

root = tk.Tk()
root.title("落下実験")

material1_var, custom1, custom_name1 = create_material_input(root, "素材1")
material2_var, custom2, custom_name2 = create_material_input(root, "素材2")

bottom_frame = ttk.LabelFrame(root, text="シミュレーション設定")
bottom_frame.pack(fill="x", padx=10, pady=5)

height_var = tk.DoubleVar(value=10.0)
gravity_var = tk.DoubleVar(value=9.81)

ttk.Label(bottom_frame, text="初期高さ（m）").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(bottom_frame, textvariable=height_var).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(bottom_frame, text="重力加速度（m/s²）").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(bottom_frame, textvariable=gravity_var).grid(row=1, column=1, padx=5, pady=5)

ttk.Button(bottom_frame, text="シミュレーション開始", command=run_simulation).grid(row=2, columnspan=2, pady=10)

root.mainloop()