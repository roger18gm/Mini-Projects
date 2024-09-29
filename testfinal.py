import pytest
from csc11_galan_final import PlayerScore, HighScore


def test_add_score():
    # Ensures that the points are being added by 10 each time
    player_score = PlayerScore()
    player_score.points = 10
    player_score.add_score()
    assert player_score.points == (20)
    player_score.add_score()
    assert player_score.points == (30)
    player_score.add_score()
    assert player_score.points == (40)
    
    # The test below will fail because when you call add_score(), the points should be 50 and not 20
    # player_score.add_score()
    # assert player_score.points == (20)
    

def test_update_highscore():
    # Ensure that the high score list is returning a list from greatest to least amount
    high_score = HighScore()
    player_score = PlayerScore()
    player_score.points = 100
    high_score.high_score_list = [50,20,150]

    high_score.update_highscore(player_score.points)
    high_score.high_score_list.sort(reverse=True)

    assert high_score.high_score_list[0] > high_score.high_score_list[1]
    assert high_score.high_score_list == [150,100,50,20]
    

pytest.main(["-v", "--tb=line", "-rN", __file__])