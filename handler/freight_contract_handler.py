class FreightContractHandler:
    def __init__(self):
        self.destination = ""
        self.cargo = {}
        self.weight = 0
        self.payout = 0

    def set_destination(self, destination):
        self.destination = destination

    def set_cargo(self, cargo):
        for cargo, weight in cargo:
            self.cargo[cargo] = weight

    def calc_weight(self):
        weight = 0
        for cargo, weight in self.db.cargo.items():
            weight += cargo[weight]
        self.db.weight = weight

    def set_payout(self, payout):
        self.db.payout = payout

    def create_contract(self, destination, cargo, payout):
        self.set_destination(destination)
        self.set_cargo(cargo)
        self.set_payout(payout)
        self.calc_weight()