class TestPlugin:
    def test_play(self, mocker) -> None:
        sender = "sender1@example.org"
        receiver = "friend1@example.org"

        # error: missing address
        msg = mocker.get_one_reply("/reversi_play", addr=sender)
        assert "❌" in msg.text

        # error: can't play against bot
        msg = mocker.get_one_reply(
            f"/reversi_play {mocker.bot.self_contact.addr}", addr=sender
        )
        assert "❌" in msg.text

        # error: can't play against yourself
        msg = mocker.get_one_reply(f"/reversi_play {sender}", addr=sender)
        assert "❌" in msg.text

        # create game group
        msg = mocker.get_one_reply(f"/reversi_play {receiver}", addr=sender)
        assert "❌" not in msg.text
        assert msg.chat.is_group()

        game_group = msg.chat

        # error: already have a game group with that player
        msg = mocker.get_one_reply(f"/reversi_play {sender}", addr=receiver)
        assert "❌" in msg.text
        assert msg.chat == game_group

    def test_new(self, mocker) -> None:
        # error: not a game group
        msg = mocker.get_one_reply("/reversi_new", group="group1")
        assert "❌" in msg.text

        # create game group
        msg = mocker.get_one_reply("/reversi_play invited_player@example.org")
        assert msg.chat.is_group()
        game_group = msg.chat

        # error: there is an active game
        msg = mocker.get_one_reply("/reversi_new", group=game_group)
        assert "❌" in msg.text

        # end current game
        msg = mocker.get_one_reply("/reversi_surrender", group=game_group)
        assert "❌" not in msg.text

        # error: sender is not a player
        msg = mocker.get_one_reply(
            "/reversi_new", addr="nonPlayer@example.org", group=game_group
        )
        assert "❌" in msg.text

        # start a new game
        msg = mocker.get_one_reply("/reversi_new", group=game_group)
        assert "❌" not in msg.text
        assert msg.chat == game_group

    def test_repeat(self, mocker) -> None:
        # error: not a game group
        msg = mocker.get_one_reply("/reversi_repeat", group="group1")
        assert "❌" in msg.text

        # create game group
        msg = mocker.get_one_reply("/reversi_play invited_player@example.org")
        assert msg.chat.is_group()
        game_group = msg.chat

        # repeat board
        msg = mocker.get_one_reply("/reversi_repeat", group=game_group)
        assert "❌" not in msg.text

        # end current game
        msg = mocker.get_one_reply("/reversi_surrender", group=game_group)
        assert "❌" not in msg.text

        # error: there is no active game
        msg = mocker.get_one_reply("/reversi_repeat", group=game_group)
        assert "❌" in msg.text

    def test_surrender(self, mocker) -> None:
        # error: not a game group
        msg = mocker.get_one_reply("/reversi_surrender", group="group1")
        assert "❌" in msg.text

        # create game group
        msg = mocker.get_one_reply("/reversi_play invited_player@example.org")
        assert msg.chat.is_group()
        game_group = msg.chat

        # error: sender is not a player
        msg = mocker.get_one_reply(
            "/reversi_surrender", addr="nonPlayer@example.org", group=game_group
        )
        assert "❌" in msg.text

        # end current game
        msg = mocker.get_one_reply("/reversi_surrender", group=game_group)
        assert "❌" not in msg.text

        # error: there is no active game
        msg = mocker.get_one_reply("/reversi_surrender", group=game_group)
        assert "❌" in msg.text

    def test_filter(self, mocker) -> None:
        player2 = "invited_player@example.org"

        # not a game group
        msgs = mocker.get_replies("a1", group="group1")
        assert not msgs

        # create game group
        msg = mocker.get_one_reply(f"/reversi_play {player2}")
        assert msg.chat.is_group()
        game_group = msg.chat

        # it isn't player2's turn
        msgs = mocker.get_replies("e3", addr=player2, group=game_group)
        assert not msgs

        # normal message ignored
        msgs = mocker.get_replies("hello", group=game_group)
        assert not msgs

        # player1's turn
        msg = mocker.get_one_reply("c4", group=game_group)
        assert "❌" not in msg.text

        # error: player2 can't play in f4
        msg = mocker.get_one_reply("f4", addr=player2, group=game_group)
        assert "❌" in msg.text

        # player2's turn
        msg = mocker.get_one_reply("c5", addr=player2, group=game_group)
        assert "❌" not in msg.text

        # end current game
        msg = mocker.get_one_reply("/reversi_surrender", group=game_group)
        assert "❌" not in msg.text

        # no active game, ignored
        msgs = mocker.get_replies("b6", group=game_group)
        assert not msgs
