from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

def main(argv):
    if len(argv) == 0:
        sys.exit("usage: sudo python3 sleepanalysis.py filename")

    filename = argv[0]

    df = pd.read_csv(filename + '.log')

    df.date = pd.to_datetime(df.date, unit='s').dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
    df['movement'] = (1 + df.gyro_x) + (1 + df.gyro_y) + (1 + df.gyro_z)
    df.sound = df.sound.rolling(20).mean()

    # print(df["date"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.movement,
                        mode='lines',
                        name='lines'))
    fig.add_trace(go.Scatter(x=df.date, y=df.sound,
                        mode='lines',
                        name='lines'))

    # fig = px.line(df, x = 'date', y = 'sound', title='Sound')
    # fig = px.line(df, x = 'date', y = 'movement', title='Movement')

    fig.show()

if __name__ == "__main__":
    import sys

    main(sys.argv[1:])