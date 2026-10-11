import unittest

from dependency_policy import approval_candidates, compatible, verified_bot_commits


def update(old="1.2.3", new="1.3.0", kind="minor", **extra):
    return {"prevVersion": old, "newVersion": new,
            "updateType": "version-update:semver-" + kind, **extra}


class PolicyTests(unittest.TestCase):
    def test_compatible_batch(self):
        self.assertTrue(compatible([update(), update("0.3.1", "0.3.2", "patch")]))

    def test_one_unsafe_update_blocks_the_entire_batch(self):
        for dependency in [update("1.2.3", "2.0.0", "major"),
                           update("0.3.1", "0.4.0"),
                           update("0.0.1", "0.0.2", "patch"),
                           update("1.2.3", "1.3.0-rc.1"),
                           update("1.2.3", "1.2.2", "patch"),
                           update(maintainerChanges=True),
                           update(kind="unknown"), {}, None]:
            with self.subTest(dependency=dependency):
                self.assertFalse(compatible([update(), dependency]))

    def test_missing_metadata_fails_closed(self):
        for metadata in [None, [], {}, [update(old="")], [update(new="")], [update(old=None)]]:
            self.assertFalse(compatible(metadata))

    def test_every_commit_must_be_a_verified_bot_commit(self):
        bot = {"author": {"login": "dependabot[bot]"},
               "commit": {"verification": {"verified": True}}}
        self.assertTrue(verified_bot_commits([bot]))
        self.assertFalse(verified_bot_commits([]))
        self.assertFalse(verified_bot_commits([bot, {"author": None}]))
        self.assertFalse(verified_bot_commits([bot, {"author": bot["author"]}]))

    def test_approval_is_bound_to_head_and_can_be_revoked(self):
        def review(number, state, head="new"):
            return {"id": number, "state": state, "commit_id": head,
                    "user": {"login": "maintainer"}}
        self.assertEqual(approval_candidates([review(1, "APPROVED", "old")], "new"), [])
        self.assertEqual(approval_candidates([review(1, "APPROVED")], "new"), ["maintainer"])
        for state in ["CHANGES_REQUESTED", "DISMISSED"]:
            self.assertEqual(approval_candidates([review(1, "APPROVED"), review(2, state)], "new"), [])
        self.assertEqual(approval_candidates([review(1, "APPROVED"), review(2, "COMMENTED")], "new"), ["maintainer"])


if __name__ == "__main__":
    unittest.main()
