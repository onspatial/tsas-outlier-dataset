def info(outlier_start_tick=0, outlier_end_tick=0, outlier_warmup_days=0, spread_days=None):
    print(f' The simulation start at day 0 and there will be {outlier_start_tick/288} days before the outliers are introduced')
    print(f' The outlier will be introduced on day {outlier_start_tick/288} and there will be a warmup period of {outlier_warmup_days} days')
    print(f' The actual outlier simulation will start on day {outlier_start_tick/288 + outlier_warmup_days} and end on day {outlier_end_tick/288}')
    print(f' The spread of the disease will last for {spread_days} days')