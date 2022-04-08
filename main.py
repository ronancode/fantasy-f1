from collections import deque

from data import costs
from data import budget_elise as budget
from data import quali_points
from data import race_points
from ratings_elise import ratings

# Generate points from ratings and add cost
info = {'teams' : {}, 'drivers': {}}
for team, team_dict in costs.items():
    team_points = 0
    for driver in costs[team]['drivers'].keys():
        rating = ratings[driver]
        if rating < len(race_points):
            points_int = race_points[rating-1] + quali_points[rating-1]
        else:
            points_int = 0
        info['drivers'][driver] = {'points': points_int, 'cost': costs[team]['drivers'][driver]}
        team_points += points_int
    info['teams'][team] = {'points': team_points, 'cost': costs[team]['cost']}

# Pick a constructor
picks_queue = deque(['', '', '', '', '', '', '', '', '', ''])
for team, team_info_dict in info['teams'].items():
    team_cost = team_info_dict['cost']
    team_points = team_info_dict['points']
    # Generate all in-budget driver combinations and find best point scoring team
    # Driver 1
    selected_drivers = ['', '', '', '', '']
    driver1_picks = []
    for driver1, driver1_dict in info['drivers'].items():
        driver1_cost = driver1_dict['cost']
        driver1_points = driver1_dict['points']
        if ((team_cost+driver1_cost) <= budget) and (driver1 not in driver1_picks):
            # Add driver
            selected_drivers[0]= driver1
            # Pick next driver
            driver2_picks = []
            for driver2, driver2_dict in info['drivers'].items():
                driver2_cost = driver2_dict['cost']
                driver2_points = driver2_dict['points']
                if ((team_cost+driver1_cost+driver2_cost) <= budget) and (driver2 not in driver2_picks) and (driver2 not in selected_drivers):
                    # Add driver
                    selected_drivers[1]= driver2
                    # Pick next driver
                    driver3_picks = []
                    for driver3, driver3_dict in info['drivers'].items():
                        driver3_cost = driver3_dict['cost']
                        driver3_points = driver3_dict['points']
                        if ((team_cost+driver1_cost+driver2_cost+driver3_cost) <= budget) and (driver3 not in driver3_picks) and (driver3 not in selected_drivers):
                            # Add driver
                            selected_drivers[2]= driver3
                            # Pick next driver
                            driver4_picks = []
                            for driver4, driver4_dict in info['drivers'].items():
                                driver4_cost = driver4_dict['cost']
                                driver4_points = driver4_dict['points']
                                if ((team_cost+driver1_cost+driver2_cost+driver3_cost+driver4_cost) <= budget) and (driver4 not in driver4_picks) and (driver4 not in selected_drivers):
                                    # Add driver
                                    selected_drivers[3]= driver4
                                    # Pick next driver
                                    driver5_picks = []
                                    for driver5, driver5_dict in info['drivers'].items():
                                        driver5_cost = driver5_dict['cost']
                                        driver5_points = driver5_dict['points']
                                        if ((team_cost+driver1_cost+driver2_cost+driver3_cost+driver4_cost+driver5_cost) <= budget) and (driver5 not in driver5_picks) and (driver5 not in selected_drivers):
                                            # Add driver
                                            selected_drivers[4]= driver5
                                            # Calculate points
                                            temp_points = team_points+driver1_points+driver2_points+driver3_points+driver4_points+driver5_points
                                            # Determine top 10 picks
                                            insert_index = None
                                            for place in range(10):
                                                if picks_queue[place] == '':
                                                    points = 0
                                                else:
                                                    points = picks_queue[place]['points']
                                                if temp_points > points:
                                                    insert_index = place
                                                    break
                                            if insert_index != None:
                                                picks = {'team': team, 'drivers': [driver1, driver2, driver3, driver4, driver5], 'points': temp_points, 'cost': team_cost+driver1_cost+driver2_cost+driver3_cost+driver4_cost+driver5_cost}
                                                # Check if pick is just reordered version of existing list
                                                record = True
                                                for pick in range(10):
                                                    pick = picks_queue[pick]
                                                    if pick != '':
                                                        if set(picks['drivers']) == set(pick['drivers']):
                                                            record = False
                                                            break
                                                if record:
                                                    picks_queue.insert(insert_index, picks)
                                                    picks_queue.pop()
                                        driver5_picks.append(driver5) 
                                driver4_picks.append(driver4) 
                        driver3_picks.append(driver3)    
                driver2_picks.append(driver2)
        driver1_picks.append(driver1)
    print(team)

for number, picks in enumerate(picks_queue):
    print('{}: {}'.format(number+1, picks))


