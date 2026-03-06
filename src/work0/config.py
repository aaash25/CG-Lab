# 仿真基础参数
NUM_PARTICLES = 400      # 集显建议从 400 开始，流畅后再增加
PARTICLE_RADIUS = 0.010   # 粒子半径
GRAVITY_STRENGTH = 0.0001 # 鼠标引力强度

# 能量损耗与环境
DRAG_COEF = 0.96            # 空气阻力 (每帧保留的速度比例)
COLLISION_ELASTICITY = 0.8  # 球体碰撞损失 (1.0 为无损，0.8 为损失 20%)
BOUNCE_COEF = -0.6          # 边界碰撞损失 (必须为负数，代表反弹)

# 画布设置
WINDOW_SIZE = (800, 800)