from datetime import datetime
import pandas as pd
import plotly.express as px
def main(argv):
    if len(argv) == 0:
        sys.exit("usage: sudo python3 sleepanalysis.py filename")

    filename = argv[0]

    df = pd.read_csv(filename + '.log')

    df.date = pd.to_datetime(df.time, unit='s').dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
    # df.sound = df.sound.rolling(20).mean()

    # print(df["date"])

    fig = px.line(df, x = 'date', y = 'sound', title='Sound')

    fig.show()

if __name__ == "__main__":
   main(sys.argv[1:])