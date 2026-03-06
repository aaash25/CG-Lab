import taichi as ti
from .config import *

# 数据结构定义
pos = ti.Vector.field(2, dtype=ti.f32, shape=NUM_PARTICLES)
vel = ti.Vector.field(2, dtype=ti.f32, shape=NUM_PARTICLES)

@ti.kernel
def init_particles():
    for i in range(NUM_PARTICLES):
        # 在中心区域随机生成，避免出生即撞墙
        pos[i] = [ti.random() * 0.6 + 0.2, ti.random() * 0.6 + 0.2]
        vel[i] = [0.0, 0.0]

@ti.kernel
def update_physics(mouse_x: float, mouse_y: float):
    # --- 第一阶段：鼠标引力与空气阻力 ---
    for i in range(NUM_PARTICLES):
        mouse_pos = ti.Vector([mouse_x, mouse_y])
        to_mouse = mouse_pos - pos[i]
        dist = to_mouse.norm(1e-5)
        
        # 鼠标引力计算
        if dist > 0.02:
            vel[i] += to_mouse.normalized() * GRAVITY_STRENGTH
        
        # 施加空气阻力并更新位置
        vel[i] *= DRAG_COEF
        pos[i] += vel[i]

    # --- 第二阶段：球体间碰撞 (O(N^2)) ---
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            rel_pos = pos[i] - pos[j]
            dist = rel_pos.norm(1e-5)
            min_dist = PARTICLE_RADIUS * 2
            
            if dist < min_dist:
                # 1. 碰撞法线
                normal = rel_pos / dist
                
                # 2. 位置修正 (解决“卡在一起”和“数值爆炸”的关键)
                overlap = min_dist - dist
                pos[i] += normal * overlap * 0.5
                pos[j] -= normal * overlap * 0.5
                
                # 3. 弹性碰撞冲量计算
                rel_v = vel[i] - vel[j]
                v_normal = rel_v.dot(normal)
                
                if v_normal < 0:
                    # 考虑碰撞损失的冲量公式
                    impulse = (1.0 + COLLISION_ELASTICITY) * v_normal * normal * 0.5
                    vel[i] -= impulse
                    vel[j] += impulse

    # --- 第三阶段：带半径补偿的边界检查 ---
    for i in range(NUM_PARTICLES):
        for k in ti.static(range(2)):
            if pos[i][k] < PARTICLE_RADIUS:
                pos[i][k] = PARTICLE_RADIUS
                vel[i][k] *= BOUNCE_COEF
            elif pos[i][k] > 1.0 - PARTICLE_RADIUS:
                pos[i][k] = 1.0 - PARTICLE_RADIUS
                vel[i][k] *= BOUNCE_COEF