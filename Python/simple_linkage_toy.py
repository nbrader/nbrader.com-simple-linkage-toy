	# make linkage program which allows you to fix an edge and move a corner within it's region of freedom (displaying this region at the same time)
		# select an unfixed corner as new dragged corner with middle click (there are always 2 options for new dragged corner)
		# select an unfixed edge as new fixed edge with right click (there are always 5 options for new fixed edge)
		# you may swing the dragged corner (with left click and mouse drag) around the circular path defined by the radius to the nearest connected fixed corner limited by the distances acheivable by the diagonal to the other fixed corner
        

#         76.5
#       _______
#      /       \
#  37 ___________ 37
#  
#         120


# revised plan
# 
# plot angles that edges directly connected to fixed edge can make on 2D graph of angle1 vs angle2
# this should demonstrate limits on the length of a two edge subsystem but also how system states can transition between paths at points where joints are maximally extended.
# make edge lengths changeable on the fly.

# Cool examples:
# example 1
    # x1 = 100
    # x2 = 190
    # x3 = 120
    # x4 = 170

# example 2
    # x1 = 360
    # x2 = 450
    # x3 = 270
    # x4 = 180

# Breaking examples:
# example 1
    # x1 = -170
    # x2 = 200
    # x3 = 370
    # x4 = -310

# example 2
    # x1 = -250
    # x2 = 210
    # x3 = 250
    # x4 = 250
    
# example 3
    # x1 = -670
    # x2 = -470
    # x3 = 560
    # x4 = -350

#(-163.046875, -283.28125, 410, 300) # broken for get_b_angles_2 and working for get_b_angles_1



import pygame
from Linear import Vec2D
from math import cos, sin, acos, asin, pi, atan2, sqrt
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
CYAN    = (  0, 255, 255)
MAGENTA = (255,   0, 255)
YELLOW  = (255, 255,   0)

def lerp(x0, x1, t):
    return x0*(1-t) + x1*t

def unlerp(x0, x1, t):
    return (t - x0)/(x1 - x0)
    
def sqr_distance(v0, v1):
    return (v1[0] - v0[0])**2 + (v1[1] - v0[1])**2

def get_b_angles_1(a, x1, x2, x3, x4):
    y_discriminant = x1**2 + x4**2 - 2*x1*x4*cos(a)
    if y_discriminant > 0:
        y  = sqrt(y_discriminant)
        b1_arg = (x1/y) * sin(a)
        if b1_arg >= -1 and b1_arg <= 1:
            b1 = asin(b1_arg)
            denom = 2*x2*y
            if denom != 0:
                b2_arg = (x2**2 + y**2 - x3**2)/denom
                if b2_arg >= -1 and b2_arg <= 1:
                    b2 = acos(b2_arg)
                    b_plus   = b1 + b2
                    b_minus  = b1 - b2
                    return (b_plus, b_minus)
    return None

def get_b_angles_2(a, x1, x2, x3, x4):
    y_discriminant = x1**2 + x4**2 - 2*x1*x4*cos(a)
    if y_discriminant > 0:
        y  = sqrt(y_discriminant)
        if a > pi:
            y = -y
        denom1 = 2*x4*y
        if denom1 != 0:
            b1_arg = (x4**2 + y**2 - x1**2)/denom1
            if b1_arg >= -1 and b1_arg <= 1:
                b1 = acos(b1_arg)
                denom2 = 2*x2*y
                if denom2 != 0:
                    b2_arg = (x2**2 + y**2 - x3**2)/denom2
                    if b2_arg >= -1 and b2_arg <= 1:
                        b2 = acos(b2_arg)
                        b_plus   = b1 + b2
                        b_minus  = b1 - b2
                        
                        b_plus += pi
                        b_plus %= 2*pi
                        b_plus -= pi
                        
                        b_minus += pi
                        b_minus %= 2*pi
                        b_minus -= pi
                        
                        if a > pi:
                            return (b_plus, b_minus)
                        else:
                            return (b_minus, b_plus)
    return None

pygame.init()

screen_width = 1024
plot_frac = screen_width/(2*pi)
screen_size = (screen_width,screen_width)

main_surface = pygame.display.set_mode(screen_size)

refresh_screen = True
refresh_screen_from_timer = True

left_mouse_pressed  = False
right_mouse_pressed = False

#         76.5
#       _______
#      /       \
#  37 ___________ 37
#  
#         120

# x1 = 250
# x2 = 250
# x3 = 250
# x4 = 250
# x1 = 360
# x2 = 450
# x3 = 270
# x4 = 180
# x1 = 185
# x2 = 185
# x3 = 600
# x4 = 382.5
# x1 = 54*2
# x2 = -41*2
# x3 = 54*2
# x4 = -41*2

x1 = -163.046875
x2 = -283.28125
x3 = 410
x4 = 300
a_of_turn = 0.25

test_x1_min = -500
test_x1_max =  500
test_x2_min = -500
test_x2_max =  500
test_steps_per_dim = 120
test_circle_width = screen_width / test_steps_per_dim

view_test_grid = True

a_pos = Vec2D((350, 500))

pygame.time.set_timer(pygame.USEREVENT, 10)

plot_points = 100
test_angles = 100

test_tol = 1

main_loop = True
while main_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
            break
        elif event.type == pygame.KEYDOWN:
            if   event.key   == pygame.K_q:
                x1 += 10
                print("increase x1")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_a:
                x1 -= 10
                print("decrease x1")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif   event.key == pygame.K_w:
                x2 += 10
                print("increase x2")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_s:
                x2 -= 10
                print("decrease x2")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif   event.key == pygame.K_e:
                x3 += 10
                print("increase x3")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_d:
                x3 -= 10
                print("decrease x3")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_r:
                x4 += 10
                print("increase x4")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_f:
                x4 -= 10
                print("decrease x4")
                print((x1,x2,x3,x4))
                refresh_screen = True
            elif event.key   == pygame.K_t:
                view_test_grid = True
                print("view_test_grid on")
                refresh_screen = True
            elif event.key   == pygame.K_g:
                view_test_grid = False
                print("dview_test_grid off")
                refresh_screen = True
        elif event.type == pygame.USEREVENT:
            a_of_turn += 0.001
            a_of_turn %= 1
            refresh_screen_from_timer = True
    
    if view_test_grid and x4 != 0:
        
        if refresh_screen:
            refresh_screen = False
            main_surface.fill(BLACK)
            for test_x1_it in range(test_steps_per_dim+1):
                for test_x2_it in range(test_steps_per_dim+1):
                    test_x1_frac = test_x1_it/(test_steps_per_dim+1)
                    test_x1 = lerp(test_x1_min, test_x1_max, test_x1_frac)
                    
                    test_x2_frac = test_x2_it/(test_steps_per_dim+1)
                    test_x2 = lerp(test_x2_min, test_x2_max, test_x2_frac)
                    
                    test_x3 = x3
                    test_x4 = x4
                    
                    # print("test_x1_it", test_x1_it)
                    # print("test_x3_it", test_x3_it)
                    # print("x2", x2)
                    # print("test_x1", test_x1)
                    # print("test_x2", test_x2)
                    # print("test_x3", test_x3)
                    # print("test_x4", test_x4)
                    
                    angles_were_given = False
                    constraint_breaking_found = False
                    for test_a_it in range(0, test_angles):
                        test_a = lerp(0, 2*pi, test_a_it/test_angles)
                        b_angles = get_b_angles_1(test_a, test_x1, test_x2, test_x3, test_x4)
                        if b_angles:
                            angles_were_given = True
                            (b_plus, b_minus) = b_angles
                            
                            b_pos = a_pos + test_x4*Vec2D((1,0))
                            a = 2*pi*a_of_turn
                            c_pos = a_pos + Vec2D.make_from_arg_mag(a, test_x1)
                            
                            d_plus_pos  = b_pos + Vec2D.make_from_arg_mag(pi - b_plus, test_x2)
                            d_minus_pos = b_pos + Vec2D.make_from_arg_mag(pi - b_minus, test_x2)
                            
                            cdplus_sqr_dist = sqr_distance(c_pos, d_plus_pos)
                            cdminus_sqr_dist = sqr_distance(c_pos, d_minus_pos)
                            
                            if abs(cdplus_sqr_dist - test_x3**2) > test_tol or abs(cdminus_sqr_dist - test_x3**2) > test_tol:
                                constraint_breaking_found = True
                                # print("cdplus_sqr_dist",cdplus_sqr_dist)
                                # print("cdminus_sqr_dist",cdminus_sqr_dist)
                                # print("test_x3**2",test_x3**2)
                                # print("abs(cdplus_sqr_dist - test_x3**2)",abs(cdplus_sqr_dist - test_x3**2))
                                # print("abs(cdminus_sqr_dist - test_x3**2)",abs(cdminus_sqr_dist - test_x3**2))
                                break
                    
                    if constraint_breaking_found and angles_were_given:
                        colour = RED
                    else:
                        colour = GREEN
                    
                    pygame.draw.circle(main_surface, colour, Vec2D((lerp(0, screen_width, test_x1_frac), lerp(0, screen_width, test_x2_frac))).round(), round(test_circle_width))
            pygame.display.flip()
            
        
    else:
        if refresh_screen or refresh_screen_from_timer:
            refresh_screen = False
            main_surface.fill(BLACK)
            
            if pygame.mouse.get_pressed()[0]:
                view_test_grid = False
                
                mouse_pos = pygame.mouse.get_pos()
                
                test_x1_frac = unlerp(0, screen_width, mouse_pos[0])
                test_x2_frac = unlerp(0, screen_width, mouse_pos[1])
                
                x1 = lerp(test_x1_min, test_x1_max, test_x1_frac)
                x2 = lerp(test_x2_min, test_x2_max, test_x2_frac)
                
                # print(x1,x2,x3,x4)
                
                angles_were_given = False
                constraint_breaking_found = False
                for test_a_it in range(0, test_angles):
                    test_a = lerp(0, 2*pi, test_a_it/test_angles)
                    b_angles = get_b_angles_2(test_a, x1, x2, x3, x4)
                    if b_angles:
                        angles_were_given = True
                        (b_plus, b_minus) = b_angles
                        
                        b_pos = a_pos + x4*Vec2D((1,0))
                        a = 2*pi*a_of_turn
                        c_pos = a_pos + Vec2D.make_from_arg_mag(a, x1)
                        
                        d_plus_pos  = b_pos + Vec2D.make_from_arg_mag(pi - b_plus, x2)
                        d_minus_pos = b_pos + Vec2D.make_from_arg_mag(pi - b_minus, x2)
                        
                        cdplus_sqr_dist = sqr_distance(c_pos, d_plus_pos)
                        cdminus_sqr_dist = sqr_distance(c_pos, d_minus_pos)
                        
                        if abs(cdplus_sqr_dist - x3**2) > test_tol or abs(cdminus_sqr_dist - x3**2) > test_tol:
                            constraint_breaking_found = True
                            # print("cdplus_sqr_dist",cdplus_sqr_dist)
                            # print("cdminus_sqr_dist",cdminus_sqr_dist)
                            # print("x3**2",x3**2)
                            # print("abs(cdplus_sqr_dist - x3**2)",abs(cdplus_sqr_dist - x3**2))
                            # print("abs(cdminus_sqr_dist - x3**2)",abs(cdminus_sqr_dist - x3**2))
                            break
                    
                # print("constraint_breaking_found",constraint_breaking_found)
                # print("angles_were_given",angles_were_given)
            
            
            
            for plot_a_it in range(0, plot_points):
                plot_a = lerp(0, 2*pi, plot_a_it/plot_points)
                b_angles = get_b_angles_1(plot_a, x1, x2, x3, x4)
                if b_angles:
                    (b_plus, b_minus) = b_angles
                    
                    a_in_screenspace = round(plot_a*plot_frac)
                    b_plus_in_screenspace = round(b_plus*plot_frac+screen_width/2) 
                    b_minus_in_screenspace = round(b_minus*plot_frac+screen_width/2)
                    
                    pygame.draw.circle(main_surface, GREEN, (a_in_screenspace, b_plus_in_screenspace),  5)
                    pygame.draw.circle(main_surface, GREEN, (a_in_screenspace, b_minus_in_screenspace), 5)
            
            b_pos = a_pos + x4*Vec2D((1,0))
            a = 2*pi*a_of_turn
            c_pos = a_pos + Vec2D.make_from_arg_mag(a, x1)
            
            pygame.draw.line(main_surface, BLUE, (a_of_turn*screen_width,0), (a_of_turn*screen_width,screen_width))
            
            b_angles = get_b_angles_1(a, x1, x2, x3, x4)
            if b_angles:
                (b_plus, b_minus) = b_angles
                d_plus_pos  = b_pos + Vec2D.make_from_arg_mag(pi - b_plus, x2)
                d_minus_pos = b_pos + Vec2D.make_from_arg_mag(pi - b_minus, x2)
                
                pygame.draw.line(main_surface, RED,     b_pos, d_plus_pos)
                pygame.draw.line(main_surface, CYAN,    c_pos, d_plus_pos)
                pygame.draw.line(main_surface, WHITE,    b_pos, d_minus_pos)
                pygame.draw.line(main_surface, MAGENTA, c_pos, d_minus_pos)
            
            
            pygame.draw.line(main_surface, GREEN,  a_pos, b_pos)
            pygame.draw.line(main_surface, YELLOW, a_pos, c_pos)
            pygame.display.flip()

pygame.quit()