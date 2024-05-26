from datetime import datetime

class ContractBase:
    def __init__(self, description, reward, expiry_date=None):
        self.description = description
        self.reward = reward
        self.expiry_date = expiry_date or datetime.now() + timedelta(days=7)
        self.status = "pending"
    
    def accept(self):
        if self.status == "pending":
            self.status = "accepted"
            return True
        return False

    def complete(self):
        if self.status == "accepted":
            self.status = "completed"
            return True
        return False

    def cancel(self):
        if self.status in ["pending", "accepted"]:
            self.status = "cancelled"
            return True
        return False

class Job(ContractBase):
    def __init__(self, description, reward, task_details, expiry_date=None):
        super().__init__(description, reward, expiry_date)
        self.task_details = task_details  

    def complete(self, player):
        """
        Completes the job and pays the player.

        Args:
            player (Object): The player who completed the job.

        Returns:
            bool: True if the job is successfully completed and paid, False otherwise.
        """
        if super().complete():
            player.db.credits += self.reward
            return True
        return False

class FreightContract(ContractBase):
    def __init__(self, sender, receiver, cargo, weight, destination, reward, expiry_date=None):
        description = f"Transport {weight} cubic meters of cargo to {destination}"
        super().__init__(description, reward, expiry_date)
        self.sender = sender
        self.receiver = receiver
        self.cargo = cargo
        self.weight = weight
        self.destination = destination

    def complete(self, player):
        """
        Completes the contract and pays the player.

        Args:
            player (Object): The player who completed the contract.

        Returns:
            bool: True if the contract is successfully completed and paid, False otherwise.
        """
        if super().complete():
            player.db.credits += self.reward
            return True
        return False

class ContractHandler:
    
    @staticmethod
    def create_job(description, reward, task_details, expiry_date=None):
        """
        Create a new job.

        Args:
            description (str): The description of the job.
            reward (int): Reward offered for completing the job.
            task_details (str): Specific details about the job.
            expiry_date (datetime, optional): Expiry date of the job. Defaults to None.

        Returns:
            Job: The created job object.
        """
        return Job(description, reward, task_details, expiry_date)
    
    @staticmethod
    def create_freight_contract(sender, receiver, cargo, weight, destination, reward, expiry_date=None):
        """
        Create a new freight contract.

        Args:
            sender (str): The sender of the contract.
            receiver (str): The receiver of the contract.
            cargo (dict): Dictionary containing the cargo to be transported.
            weight (float): Weight of the cargo in cubic meters.
            destination (str): Destination of the cargo.
            reward (int): Reward offered for completing the contract.
            expiry_date (datetime, optional): Expiry date of the contract. Defaults to None.

        Returns:
            FreightContract: The created freight contract object.
        """
        return FreightContract(sender, receiver, cargo, weight, destination, reward, expiry_date)
    
    @staticmethod
    def update_contract(contract, **kwargs):
        """
        Update an existing contract with new information.

        Args:
            contract (ContractBase): The contract to update.
            **kwargs: Keyword arguments representing attributes to update.

        Returns:
            ContractBase: The updated contract object.
        """
        for key, value in kwargs.items():
            setattr(contract, key, value)
        return contract

    @staticmethod
    def cancel_contract(contract):
        """
        Cancel an existing contract.

        Args:
            contract (ContractBase): The contract to cancel.

        Returns:
            bool: True if the contract is successfully canceled, False otherwise.
        """
        return contract.cancel()
    
    @staticmethod
    def accept_contract(contract):
        """
        Accept a contract.

        Args:
            contract (ContractBase): The contract to accept.

        Returns:
            bool: True if the contract is successfully accepted, False otherwise.
        """
        return contract.accept()
