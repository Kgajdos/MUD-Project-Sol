class FreightContractHandler:
    def __init__(self):
        self.destination = ""
        self.cargo = {}
        self.weight = 0
        self.payout = 0

    def set_destination(self, destination):
        self.destination = destination

    def set_cargo(self, cargo):
        for item, weight in cargo.items():
            self.cargo[item] = weight

    def calc_weight(self):
        weight = 0
        for item_weight in self.cargo.values():
            weight += item_weight
        self.weight = weight

    def set_payout(self, payout):
        self.payout = payout

    def create_contract(self, destination, cargo, payout):
        self.set_destination(destination)
        self.set_cargo(cargo)
        self.set_payout(payout)
        self.calc_weight()

    def accept_contract(self, ship):
        # Assuming ship.db.contracts is a list
        if not hasattr(ship.db, "contracts"):
            ship.db.contracts = []

        ship.db.contracts.append(self)

        # Assuming ship.db.cargo is a dictionary
        if not hasattr(ship.db, "cargo"):
            ship.db.cargo = {}

        for item, weight in self.cargo.items():
            ship.db.cargo[item] = ship.db.cargo.get(item, 0) + weight

        ship.db.pilot.msg(f"Contract accepted. Cargo loaded onto {ship.key}.")

    def complete_contract(self, ship):
        if self in ship.db.contracts:
            ship.db.contracts.remove(self)

            for item, weight in self.cargo.items():
                if item in ship.db.cargo:
                    ship.db.cargo[item] -= weight
                    if ship.db.cargo[item] <= 0:
                        del ship.db.cargo[item]

            ship.db.pilot.msg(f"Contract to {self.destination} completed.")

    def payout(self, player):
        player.db.credits += self.payout
        player.msg(f"{player.key} has been paid {self.payout} credits.")
