import taichi as ti
ti.init(arch=ti.vulkan)
from .physics import *
from .config import *

def main():
    # 集显用户推荐使用 ti.vulkan 或 ti.auto
    
    
    init_particles()
    
    window = ti.ui.Window("Modern CG Lab - Physics Demo", WINDOW_SIZE)
    canvas = window.get_canvas()
    
    print("仿真启动！移动鼠标以吸引粒子。")
    
    while window.running:
        # 1. 获取交互
        mouse = window.get_cursor_pos()
        
        # 2. 物理步 (如果想要更硬的碰撞，每帧可以多跑几次 update)
        update_physics(mouse[0], mouse[1])
        
        # 3. 渲染
        canvas.set_background_color((0.08, 0.08, 0.12)) # 深灰蓝背景
        canvas.circles(pos, radius=PARTICLE_RADIUS, color=(0.3, 0.7, 1.0))
        
        window.show()

if __name__ == "__main__":
    main()