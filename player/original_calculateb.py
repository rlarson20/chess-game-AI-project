
    def calculateb(self,gametiles):
        value=0
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.tostring()=='P':
                        value=value-100

                    if gametiles[y][x].pieceonTile.tostring()=='N':
                        value=value-350

                    if gametiles[y][x].pieceonTile.tostring()=='B':
                        value=value-350

                    if gametiles[y][x].pieceonTile.tostring()=='R':
                        value=value-525

                    if gametiles[y][x].pieceonTile.tostring()=='Q':
                        value=value-1000

                    if gametiles[y][x].pieceonTile.tostring()=='K':
                        value=value-10000

                    if gametiles[y][x].pieceonTile.tostring()=='p':
                        value=value+100

                    if gametiles[y][x].pieceonTile.tostring()=='n':
                        value=value+350

                    if gametiles[y][x].pieceonTile.tostring()=='b':
                        value=value+350

                    if gametiles[y][x].pieceonTile.tostring()=='r':
                        value=value+525

                    if gametiles[y][x].pieceonTile.tostring()=='q':
                        value=value+1000

                    if gametiles[y][x].pieceonTile.tostring()=='k':
                        value=value+10000

        return value
