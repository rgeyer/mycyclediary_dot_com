class bike_stats():
    def __init__(self, meters_distance=0, time=0, meters_elevation=0, meters_per_second_avg_speed=0, kjs=0, records=0):
        self.meters_distance = meters_distance
        self.time = time
        self.meters_elevation = meters_elevation
        self.meters_per_second_avg_speed = meters_per_second_avg_speed
        self.kjs = kjs
        self.records = records

    def __add__(self, other):
        return bike_stats(
            meters_distance =               self.meters_distance + other.meters_distance,
            time =                          self.time + other.time,
            meters_elevation =              self.meters_elevation + other.meters_elevation,
            meters_per_second_avg_speed =   self.meters_per_second_avg_speed + other.meters_per_second_avg_speed,
            kjs =                           self.kjs + other.kjs,
            records =                       self.records + other.records
        )
