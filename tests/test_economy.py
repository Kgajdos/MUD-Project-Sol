from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses.corporations import create_corporation
from typeclasses.contract import ContractHandler


class TestEconomy(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        # create a leader account/character and an employee/pilot
        self.leader = create.create_object("typeclasses.characters.Character", key="Leader")
        self.employee = create.create_object("typeclasses.characters.Character", key="Worker")
        self.pilot = create.create_object("typeclasses.characters.Character", key="Pilot")

        # ensure starting credits are zero for deterministic assertions
        for obj in (self.leader, self.employee, self.pilot):
            obj.db.credits = 0

        # create a corporation with the leader as CEO
        self.corp = create_corporation("TestCorp", self.leader)

    def test_create_corporation(self):
        # leader should be recorded in both employees and leaders maps
        assert self.leader in self.corp.db.employees
        assert self.leader in self.corp.db.leaders
        # leader should reference the corporation
        assert getattr(self.leader.db, "corporation", None) is self.corp

    def test_post_job_and_complete(self):
        # Post a job and accept/complete it
        job = self.corp.post_job("Repair hull", 500, "Patch the hull")
        assert job in self.corp.db.jobs
        # accept the job first
        assert ContractHandler.accept_contract(job) is True
        # complete the job and pay the employee
        self.corp.complete_job(job, self.employee)
        # employee should have been paid and job removed
        assert self.employee.db.credits == 500
        assert job not in self.corp.db.jobs
        assert job.status == "completed"

    def test_post_freight_contract_and_freighter_accept(self):
        # Post a freight contract and have a freighter accept it
        cargo = {"iron": 10}
        contract = self.corp.post_contract(self.leader, self.corp, cargo, weight=10, destination="Alpha", reward=1000)
        # assert contract in self.corp.db.contracts
        # Corporation stores a serializable summary in db.contracts; check by id
        assert any(s.get('id') == id(contract) for s in (self.corp.db.contracts or []))

        # create a freighter ship
        freighter = create.create_object("typeclasses.ships.Freighter", key="BigHaul")
        # accept the contract using the freighter
        accepted = freighter.accept_contract(contract)
        assert accepted is True
        # cargo should have been merged into the ship
        assert freighter.db.cargo is not None
        assert freighter.db.cargo.get("iron", 0) == 10
        assert freighter.db.cargohold >= 10
        assert contract.status == "accepted"

        # complete the contract and pay the pilot/employee who performed it
        # use self.pilot as the recipient of the reward
        self.corp.complete_contract(contract, self.pilot)
        assert self.pilot.db.credits == 1000
        # After completion the serializable summary should be removed
        assert not any(s.get('id') == id(contract) for s in (self.corp.db.contracts or []))
        assert contract.status == "completed"
