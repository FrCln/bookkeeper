@pytest.mark.parametrize("repo", MemoryRepository(), SQLiteRepository(...))
def test_crud(repo, custom_class):
    # то же самое
