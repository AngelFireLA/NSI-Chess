from  engine.partie import Partie

# Partie exemple
p = Partie()
p.setup_from_fen("default")


p.run(menu=True)
