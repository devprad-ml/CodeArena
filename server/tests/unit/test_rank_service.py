from app.services.rank_service import RankService


class TestRankService:
    def setup_method(self):
        self.rank_service = RankService()

    def test_correct_first_attempt_points(self):
        points = self.rank_service.calculate_submission_points(is_correct=True, attempt_number=1)
        assert points == 25

    def test_correct_after_wrong_attempts(self):
        points = self.rank_service.calculate_submission_points(is_correct=True, attempt_number=3)
        # 25 + (2 * -5) = 15
        assert points == 15

    def test_correct_minimum_points(self):
        points = self.rank_service.calculate_submission_points(is_correct=True, attempt_number=10)
        # 25 + (9 * -5) = -20, but minimum is 5
        assert points == 5

    def test_wrong_submission_penalty(self):
        points = self.rank_service.calculate_submission_points(is_correct=False, attempt_number=1)
        assert points == -5

    def test_pirate_rank_rookie(self):
        info = self.rank_service.get_rank_info("pirate", 0)
        assert info["rank_name"] == "Rookie"

    def test_pirate_rank_super_rookie(self):
        info = self.rank_service.get_rank_info("pirate", 100)
        assert info["rank_name"] == "Super Rookie"

    def test_pirate_rank_supernova(self):
        info = self.rank_service.get_rank_info("pirate", 200)
        assert info["rank_name"] == "Supernova"

    def test_marine_rank_ensign(self):
        info = self.rank_service.get_rank_info("marine", 0)
        assert info["rank_name"] == "Ensign"

    def test_rank_up_detected(self):
        ranked_up, details = self.rank_service.check_rank_up("pirate", 95, 105)
        assert ranked_up is True
        assert details["old_rank"] == "Rookie"
        assert details["new_rank"] == "Super Rookie"

    def test_no_rank_up(self):
        ranked_up, details = self.rank_service.check_rank_up("pirate", 50, 75)
        assert ranked_up is False

    def test_supreme_pirate_qualification_fails(self):
        user_stats = {
            "total_points": 600,
            "first_try_rate": 0.5,
            "expert_problems_solved": 3,
            "categories_completed": ["arrays"],
            "current_streak": 2,
        }
        qualified, details = self.rank_service.check_supreme_rank_qualification(
            "pirate", user_stats
        )
        assert qualified is False

    def test_supreme_pirate_qualification_succeeds(self):
        user_stats = {
            "total_points": 700,
            "first_try_rate": 0.85,
            "expert_problems_solved": 15,
            "categories_completed": [
                "arrays", "strings", "linked_lists", "stacks_queues",
                "trees", "graphs", "dynamic_programming", "recursion",
                "sorting_searching", "bit_manipulation",
            ],
            "current_streak": 10,
        }
        qualified, details = self.rank_service.check_supreme_rank_qualification(
            "pirate", user_stats
        )
        assert qualified is True
