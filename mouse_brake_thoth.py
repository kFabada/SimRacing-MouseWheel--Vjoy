if starting:    
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 5
    
    def set_button(button, key):
        if keyboard.getKeyDown(key):
            v.setButton(button, True)
        else:
            v.setButton(button, False)
    
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max

    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1
    
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8

    # =============================================================================================
    # Axis inversion settings (multiplier): normal = 1; inverted = -1
    # =============================================================================================
    global throttle_inversion, braking_inversion, clutch_inversion
    throttle_inversion = 1
    braking_inversion = 1
    clutch_inversion = 1
    
    # =============================================================================================
    # Mouse settings
    # =============================================================================================
    global mouse_sensitivity, sensitivity_center_reduction
    mouse_sensitivity = 5
    sensitivity_center_reduction = 2.3
    
    # =============================================================================================
    # Ignition cut settings
    # =============================================================================================
    global ignition_cut_time, ignition_cut_elapsed_time
    ignition_cut_enabled = True
    ignition_cut_time = 100
    ignition_cut_elapsed_time = 0
    
    global ignition_cut, ignition_cut_released
    # Init values, do not change
    ignition_cut = False
    ignition_cut_released = True
    
    # =============================================================================================
    # Steering settings
    # =============================================================================================
    global steering, steering_max, steering_min, steering_center_reduction    
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 0.4
    
    # =============================================================================================
    # Throttle settings
    # =============================================================================================
    global throttle_blip_enabled
    throttle_blip_enabled = True
    
    # In milliseconds
    throttle_increase_time = 110
    throttle_increase_time_after_ignition_cut = 0
    throttle_increase_time_blip = 50
    throttle_decrease_time = 100
    
    global throttle, throttle_max, throttle_min, mouse_vertical_min, mouse_vertical_max
    # Init values, do not change
    throttle_max = int32_max * throttle_inversion
    throttle_min = int32_min * throttle_inversion
    throttle = throttle_min
    mouse_vertical_min = -1  # Define o valor mínimo para o movimento vertical do mouse
    mouse_vertical_max = 1   # Define o valor máximo para o movimento vertical do mouse
    
    global throttle_increase_rate, throttle_decrease_rate
    # Set throttle behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    throttle_increase_rate = calculate_rate(throttle_max, throttle_increase_time)
    throttle_increase_rate_after_ignition_cut = calculate_rate(throttle_max, throttle_increase_time_after_ignition_cut) 
    throttle_increase_rate_blip = calculate_rate(throttle_max, throttle_increase_time_blip)
    throttle_decrease_rate = calculate_rate(throttle_max, throttle_decrease_time) * -1
    
    # =============================================================================================
    # Braking settings
    # =============================================================================================
    # In milliseconds
    braking_increase_time = 100
    braking_decrease_time = 100
    
    global braking, braking_max, braking_min, mouse_vertical_min, mouse_vertical_max
    # Init values, do not change
    braking_max = int32_max * braking_inversion
    braking_min = int32_min * braking_inversion
    braking = braking_min
    mouse_vertical_min = -1  # Define o valor mínimo para o movimento vertical do mouse
    mouse_vertical_max = 1   # Define o valor máximo para o movimento vertical do mouse
    
    global braking_increase_rate, braking_decrease_rate
    # Set braking behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    braking_increase_rate = calculate_rate(braking_max, braking_increase_time)
    braking_decrease_rate = calculate_rate(braking_max, braking_decrease_time) * -1
    
    # =============================================================================================
    # Clutch settings
    # =============================================================================================   
    # In milliseconds
    clutch_increase_time = 0
    clutch_decrease_time = 50
    
    global clutch, clutch_max, clutch_min
    # Init values, do not change
    clutch_max = int32_max * clutch_inversion
    clutch_min = int32_min * clutch_inversion
    clutch = clutch_min
    
    global clutch_increase_rate, clutch_decrease_rate
    # Set clutch behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    clutch_increase_rate = calculate_rate(clutch_max, clutch_increase_time)
    clutch_decrease_rate = calculate_rate(clutch_max, clutch_decrease_time) * -1


# assign button
#vJoy[0].setButton(0,int(mouse.leftButton))
#vJoy[0].setButton(1,int(mouse.rightButton))
vJoy[0].setButton(1,int(keyboard.getKeyDown(Key.D)))
vJoy[0].setButton(2,int(keyboard.getKeyDown(Key.A)))
vJoy[0].setButton(3,int(keyboard.getKeyDown(Key.E)))
vJoy[0].setButton(4,int(keyboard.getKeyDown(Key.R)))
vJoy[0].setButton(5,int(keyboard.getKeyDown(Key.T)))
vJoy[0].setButton(6,int(keyboard.getKeyDown(Key.Space)))
vJoy[0].setButton(7,int(keyboard.getKeyDown(Key.F)))
vJoy[0].setButton(8,int(keyboard.getKeyDown(Key.G)))
vJoy[0].setButton(9,int(keyboard.getKeyDown(Key.H)))
vJoy[0].setButton(10,int(keyboard.getKeyDown(Key.B)))
vJoy[0].setButton(11,int(keyboard.getKeyDown(Key.N)))
vJoy[0].setButton(12,int(keyboard.getKeyDown(Key.X)))
# =================================================================================================
# LOOP START
# =================================================================================================

# =================================================================================================
# Steering logic
# =================================================================================================
if steering > 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_max))
elif steering < 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_min))

steering = steering + ((float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction)

if steering > steering_max:
    steering = steering_max
elif steering < steering_min:
    steering = steering_min

v.x = int(round(steering))

# =================================================================================================
# Clutch logic
# =================================================================================================
if keyboard.getKeyDown(Key.C):
    clutch = clutch + clutch_increase_rate
else:
    clutch = clutch + clutch_decrease_rate

if clutch > clutch_max * clutch_inversion:
    clutch = clutch_max * clutch_inversion
elif clutch < clutch_min * clutch_inversion:
    clutch = clutch_min * clutch_inversion

v.z = clutch

# =================================================================================================
# Throttle and Brake logic using vertical mouse movement
# =================================================================================================

# Capturando o movimento vertical do mouse
mouse_vertical = mouse.deltaY * mouse_sensitivity

# Ajustando o throttle com base no movimento vertical do mouse
if mouse_vertical < 0:
    throttle_increase = throttle_increase_rate * abs(mouse_vertical) / mouse_vertical_max
    throttle += throttle_increase * system.threadExecutionInterval / 1000
else:
    throttle_decrease = throttle_decrease_rate * mouse_vertical / mouse_vertical_min
    throttle -= throttle_decrease * system.threadExecutionInterval / 1000

# Limitando o throttle aos valores máximo e mínimo
if throttle > throttle_max:
    throttle = throttle_max
elif throttle < throttle_min:
    throttle = throttle_min

# Ajustando o brake com base no movimento vertical inverso do mouse
if mouse_vertical > 0:
    braking_increase = braking_increase_rate * abs(mouse_vertical) / mouse_vertical_max
    braking += braking_increase * system.threadExecutionInterval / 1000
else:
    braking_decrease = braking_decrease_rate * mouse_vertical / mouse_vertical_min
    braking -= braking_decrease * system.threadExecutionInterval / 1000

# Limitando o brake aos valores máximo e mínimo
if braking > braking_max:
    braking = braking_max
elif braking < braking_min:
    braking = braking_min

# Atribuindo os valores apropriados às saídas do VJoy
v.y = throttle * throttle_inversion
v.rz = braking * braking_inversion

# =================================================================================================
# Braking logic
# =================================================================================================

if braking > braking_max * braking_inversion:
    braking = braking_max * braking_inversion
elif braking < braking_min * braking_inversion:
    braking = braking_min * braking_inversion

v.rz = braking

# =================================================================================================
# Buttons post-throttle logic
# =================================================================================================
#set_button(look_left_button, look_left_key)
#set_button(look_right_button, look_right_key)
#set_button(look_back_button, look_back_key)
#set_button(change_view_button, change_view_key)
#set_button(indicator_left_button, indicator_left_key)
#set_button(indicator_right_button, indicator_right_key)

# =================================================================================================
# PIE diagnostics logic
# =================================================================================================
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.rz)
diagnostics.watch(v.slider)
diagnostics.watch(steering_center_reduction)
diagnostics.watch(throttle_blip_enabled)
diagnostics.watch(ignition_cut_enabled)
