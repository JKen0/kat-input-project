import KATData.FetchKATData as FetchKAT

kat_config = FetchKAT.FetchKATData(-1, -1)

while True:
    LF_roll , LF_pitch, RF_roll, RF_pitch = kat_config.getData()

    print(LF_roll , LF_pitch, RF_roll, RF_pitch)
