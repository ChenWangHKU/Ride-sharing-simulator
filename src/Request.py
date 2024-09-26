'''
The object of a single request
The whole requests are operated in the Contral Center
''' 
class Request:
    def __init__(self,
                cfg,
                id = 0,
                send_request_timepoint = 0,
                pickup_position = 0,
                dropoff_position = 0,
                pickup_grid_id = 0,
                dropoff_grid_id = 0,
                original_travel_time = 0,
                original_travel_distance = 0,
                num_person = 1):
        self.cfg = cfg
        self.id = id
        self.send_request_timepoint = send_request_timepoint
        # origin and destination node id
        self.pickup_position = pickup_position
        self.dropoff_position = dropoff_position
        # grid id
        self.pickup_grid_id = pickup_grid_id
        self.dropoff_grid_id = dropoff_grid_id
        # travel distance and time
        self.original_travel_distance = original_travel_distance
        self.original_travel_time = original_travel_time
        # todo... (we assume that there is only one person in each request)
        self.num_person = num_person # There may be more than 1 person in some requests
        self.max_tol_num_person = 1
        

        
        ################################  These perameters can be redefined  ###################################
        # behaviors
        self.max_tol_assign_time = self.cfg.REQUEST.BEHAVIORS.max_assign_time
        self.cancel_prob_assign = self.cfg.REQUEST.BEHAVIORS.cancel_prob_assign
        self.max_tol_pickup_time = self.cfg.REQUEST.BEHAVIORS.max_pickup_time
        self.cancel_prob_pickup =  self.cfg.REQUEST.BEHAVIORS.cancel_prob_pickup
        self.max_tol_vehicle_capacity =  self.cfg.REQUEST.BEHAVIORS.max_tol_vehicle_capacity # Some passengers can not stand full capacity of a vehicle
        
        # constraints
        self.max_con_assign_time = self.cfg.REQUEST.CONSTRAINTS.max_assign_time
        self.max_con_pickup_time = self.cfg.REQUEST.CONSTRAINTS.max_pickup_time
        self.max_con_travel_time = self.cfg.REQUEST.CONSTRAINTS.max_travel_time_mul * self.original_travel_time
        self.max_con_travel_diatance = self.cfg.REQUEST.CONSTRAINTS.max_travel_dis_mul * self.original_travel_distance
        ################################  These perameters can be redefined  ###################################

        self.MAX_DROPOFF_DELAY = self.max_con_travel_time - self.original_travel_time


        # Record the status of the request
        self.finish_assign = False
        self.finish_pickup = False
        self.finish_dropoff = False
        self.assign_timepoint = 0
        self.pickup_timepoint = 0
        self.dropoff_timepoint = 0
        self.vehicle_id = None

        # Record the time and distance of the request on the vehicle
        self.time_on_vehicle = 0
        self.distance_on_vehicle = 0
        
        # todo...
        self.max_tol_price = 0
        self.comfortable_value = 0
    

    # Calculate the price of request
    # We refer: https://www.nyc.com/visitor_guide/taxis.75827/
    def CalculatePrice(self):
        initial_charge = 2.5
        mileage_charge = 0.4  # per 0.2 mile
        waiting_charge = 0.4  # per 60 seconds, which may be used when considering congestion
        # 8 p.m. - 6 a.m.  --> 7 nights
        night_surcharge = 0.5 if self.send_request_timepoint > 20*3600 or self.send_request_timepoint < 6*3600 else 0.0
        # 4 - 8 p.m.   --> weekdays only, excluding holidays
        peak_hour_price = 1.0 if self.send_request_timepoint > 16*3600 and self.send_request_timepoint < 20*3600 else 0.0
        
        total_price =  initial_charge + self.original_travel_distance / (1609 / 5) * mileage_charge + night_surcharge + peak_hour_price
        
        return 0.7*total_price
    
    
    
    # function: Calculate the maximum price that passenger(s) can accept
    # params: todo...(May be travel time, travel distance, the number of passengers, etc.)
    # return: maximum tolerant price
    # Note: The maximum price may also be estimated from a specific distribution function or assigned ahead of time
    def MaxTolPrice(self):
        pass

    # function: Calculate the comfortable value of passenger(s) and evaluate comfort
    # params: todo...(May be travel time, travel distance, the number of passengers, etc.)
    # return: comfortable value
    def ComfortableValue(self):
        pass