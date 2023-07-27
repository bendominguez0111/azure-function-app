import datetime
import logging

import pandas as pd
import nfl_data_py as nfl

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # get the top 5 players by air yards in 2022
    df = nfl.import_pbp_data(years=[2022])
    air_yards = df.groupby(['receiver_player_id', 'receiver_player_name'], as_index=False)\
        ['air_yards'].sum().sort_values(by='air_yards', ascending=False).head(5)
    
    print(air_yards)