from  engine.partie import Partie

# Partie exemple
p = Partie()
p.setup_from_fen("rgbvkbnr/tppppppi/pp4pp/8/8/PP4PP/TPPPPPPI/RGBVKBNR")


p.run(menu=True)
