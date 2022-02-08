from pygame.sprite import Sprite
from pygame import Rect

normals = ((-1, 0),
           (0, -1),
           (1, 0),
           (0, 1))

# normals order = left, bottom, right, up
def proj_min_max(rect: Rect):
    left = rect.left
    right = rect.right
    top = rect.bottom
    bottom = rect.top

    # (min, max)
    projs = ((-right, -left),
             (-top, -bottom),
             (left, right),
             (bottom, top))
    
    return projs

# Sprite.rect = top, left, width, height
def AABB_collision_resolution(dynamic_obj: Sprite, static_obj: Sprite):
    dynamic_projs = proj_min_max(dynamic_obj.rect)
    static_projs = proj_min_max(static_obj.rect)
    
    # find least penetration
    min_p = float('inf')
    min_axis_p = None
    
    for i in range(4):
        p = static_projs[i][1] - dynamic_projs[i][0]
        
        if p <= 0:
            return
        
        if p < min_p:
            min_p = p
            min_axis_p = normals[i]
            
    # resolve
    dynamic_obj.pos.x += min_axis_p[0] * min_p
    dynamic_obj.pos.y += min_axis_p[1] * min_p
    dynamic_obj.update_rect()