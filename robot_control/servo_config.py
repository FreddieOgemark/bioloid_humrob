import math

# home position in encoder ticks for the servo.

servo_param = {
    1: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,    
        'max_ang': math.radians( 148 ),
        'min_ang': math.radians( -148 )
       }, 
    2: {                        # Tilting Hokuyo on El-E
        'home_encoder': 512,
        'max_ang': math.radians( 148 ),
        'min_ang': math.radians( -148 )
       }, 
    3: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,     
       }, 
    4: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
       }, 
    5: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    6: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    7: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
       }, 
    8: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    9: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    10: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
       }, 
    11: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    12: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    13: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
       }, 
    14: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    15: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    16: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
       }, 
    17: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    18: {                        # Default for new servo.  Please issue 'new_servo.write_id(new_id)' and setup your own home position!
        'home_encoder': 512,
        'max_ang': math.radians( 100 ),
        'min_ang': math.radians( -100 )      
       }, 
    19: {                        # Desktop System UTM
        'home_encoder': 633,
        'flipped': True
        },
    20: {                        # Desktop System Tilt
        'home_encoder': 381
        },
    21: {                        # Desktop System Pan
        'home_encoder': 589
        },
    22: {                        # Desktop System Roll
        'home_encoder': 454
        },
    23: {                        # Dinah Top
        'home_encoder': 379
        },
    24: {                        # Dinah Bottom
        'home_encoder': 365
        },
    25: {                        # Meka top Pan
        'home_encoder': 500
        },
    26: {                        # Meka top Tilt
        'home_encoder': 400
        },
    27: {                        # PR2 RFID Left Pan
        'home_encoder': 512
        },
    28: {                        # PR2 RFID Left Tilt
        'home_encoder': 512
        },
    29: {                        # PR2 RFID Right Pan
        'home_encoder': 544
        },
    30: {                        # PR2 RFID Right Tilt
        'home_encoder': 504
        }

}

