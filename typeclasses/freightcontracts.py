from typeclasses.objects import Object

class FreightContract(Object):
    def at_object_creation(self):
        self.db.sender
        self.db.receiver
        self.db.cargo
        self.db.reward
        self.db.expiration

    def create_contract(self, sender, receiver, cargo, reward, expiration):
        """
        Create a freight contract.

        Args:
            sender (Object): The player who initiates the contract.
            receiver (Object): The player or corporation who will receive the cargo.
            cargo (dict): A dictionary containing the cargo to be transported.
                The keys are the resource names, and the values are the quantities.
            reward (int): The amount of reward offered for successfully fulfilling the contract.

        Notes:
            - The sender must be a player object.
            - The receiver can be either a player object or a corporation object.
            - The cargo parameter should usually be a dictionary specifying the resources to be transported.
            - The reward is an integer value representing the amount of credits offered as payment.

        Example:
            # Create a contract for PlayerA to deliver resources to CorporationB for a reward of 500 credits.
            player_a = Player.key
            corp_b = Corporation.key
            resources_to_transport = {"iron": 100, "gold": 50}
            contract_reward = 500
            player_a.create_contract(sender=player_a, receiver=corp_b, cargo=resources_to_transport, reward=contract_reward)
    """
        self.db.sender = sender
        self.db.receiver = receiver
        self.db.cargo = cargo
        self.db.reward = reward
        self.db.expiration = expiration

        