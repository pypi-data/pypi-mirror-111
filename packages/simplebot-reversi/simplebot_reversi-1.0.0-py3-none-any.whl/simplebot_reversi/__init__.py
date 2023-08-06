import os

import simplebot
from deltachat import Chat, Contact, Message
from pkg_resources import DistributionNotFound, get_distribution
from simplebot import DeltaBot
from simplebot.bot import Replies

from .orm import Game, init, session_scope
from .reversi import BLACK, WHITE, Board

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0.0.dev0-unknown"


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    path = os.path.join(os.path.dirname(bot.account.db_path), __name__)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "sqlite.db")
    init(f"sqlite:///{path}")


@simplebot.hookimpl
def deltabot_member_removed(bot: DeltaBot, chat: Chat, contact: Contact) -> None:
    with session_scope() as session:
        game = session.query(Game).filter_by(chat_id=chat.id).first()
        if game:
            members = [contact.addr for contact in chat.get_contacts()]
            players = (bot.self_contact.addr, game.p1, game.p2)
            if any(map(lambda addr: addr not in members, players)):
                session.delete(game)
                try:
                    chat.remove_contact(bot.self_contact)
                except ValueError:
                    pass


@simplebot.filter(name=__name__)
def filter_messages(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Process move coordinates in Reversi game groups"""
    if len(message.text) != 2 or not message.text.isalnum():
        return

    with session_scope() as session:
        game = session.query(Game).filter_by(chat_id=message.chat.id).first()
        if game is None or game.board is None:
            return

        board = Board(game.board)

        player = (
            BLACK if game.black_player == message.get_sender_contact().addr else WHITE
        )
        if board.turn == player:
            try:
                board.move(message.text)
                game.board = board.export()
                replies.add(text=_run_turn(bot, game))
            except (ValueError, AssertionError):
                replies.add(text="❌ Invalid move!", quote=message)


@simplebot.command
def reversi_play(
    bot: DeltaBot, payload: str, message: Message, replies: Replies
) -> None:
    """Invite a friend to play Reversi.

    Example: /reversi_play friend@example.com
    """
    if not payload or "@" not in payload:
        replies.add(
            text="❌ Invalid address. Example:\n/reversi_play friend@example.com",
            quote=message,
        )
        return

    if payload == bot.self_contact.addr:
        replies.add(text="❌ Sorry, I don't want to play", quote=message)
        return

    sender = message.get_sender_contact()
    receiver = bot.get_contact(payload)
    if sender == receiver:
        replies.add(text="❌ You can't play with yourself", quote=message)
        return

    p1, p2 = sorted([sender.addr, receiver.addr])
    with session_scope() as session:
        game = session.query(Game).filter_by(p1=p1, p2=p2).first()
        if game is None:  # first time playing with this contact
            board = Board()
            chat = bot.create_group(
                f"🔴 {sender.addr} 🆚 {receiver.addr}", [sender, receiver]
            )
            game = Game(
                p1=p1,
                p2=p2,
                chat_id=chat.id,
                board=board.export(),
                black_player=sender.addr,
            )
            session.add(game)
            text = f"Hello {receiver.name},\nYou have been invited by {sender.name} to play Reversi.\n\n{board.get_disk(BLACK)}: {sender.name}\n{board.get_disk(WHITE)}: {receiver.name}\n\n"
            replies.add(text=text + _run_turn(bot, game), chat=chat)
        else:
            text = f"❌ You already have a game group with {payload}"
            replies.add(text=text, chat=bot.get_chat(game.chat_id))


@simplebot.command
def reversi_surrender(message: Message, replies: Replies) -> None:
    """End the Reversi game in the group it is sent."""
    sender = message.get_sender_contact()
    with session_scope() as session:
        game = session.query(Game).filter_by(chat_id=message.chat.id).first()
        if game is None or sender.addr not in (game.p1, game.p2):
            replies.add(text="❌ This is not your game group", quote=message)
        elif game.board is None:
            replies.add(text="❌ There is no active game", quote=message)
        else:
            game.board = None
            replies.add(
                text=f"🏳️ Game Over.\n{sender.name} surrenders.\n\n▶️ Play again? /reversi_new"
            )


@simplebot.command
def reversi_new(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Start a new Reversi game in the current game group."""
    sender = message.get_sender_contact()
    with session_scope() as session:
        game = session.query(Game).filter_by(chat_id=message.chat.id).first()
        if game is None or sender.addr not in (game.p1, game.p2):
            replies.add(text="❌ This is not your game group", quote=message)
        elif game.board is None:
            board = Board()
            game.board = board.export()
            game.black_player = sender.addr
            p2_name = bot.get_contact(
                game.p2 if sender.addr == game.p1 else game.p1
            ).name
            text = f"▶️ Game started!\n{board.get_disk(BLACK)}: {sender.name}\n{board.get_disk(WHITE)}: {p2_name}\n\n"
            replies.add(text=text + _run_turn(bot, game))
        else:
            replies.add(text="❌ There is an active game already", quote=message)


@simplebot.command
def reversi_repeat(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send game board again."""
    with session_scope() as session:
        game = session.query(Game).filter_by(chat_id=message.chat.id).first()
        if not game:
            text = "❌ This is not a Reversi game group"
        elif not game.board:
            text = "❌ There is no active game"
        else:
            text = _run_turn(bot, game)
        replies.add(text=text)


def _run_turn(bot: DeltaBot, game: Game) -> str:
    board = Board(game.board)
    result = board.result()
    if result["status"] == -1:  # Game Over
        game.board = None
        if result[BLACK] == result[WHITE]:
            text = "🤝 Game over.\nIt is a draw!\n\n"
        else:
            if result[BLACK] > result[WHITE]:
                winner = (
                    f"{board.get_disk(BLACK)} {bot.get_contact(game.black_player).name}"
                )
            else:
                white_player = game.p2 if game.black_player == game.p1 else game.p1
                winner = f"{board.get_disk(WHITE)} {bot.get_contact(white_player).name}"
            text = f"🏆 Game over.\n{winner} wins!\n\n"
        text += "\n\n".join(
            (str(board), board.get_score(), "▶️ Play again? /reversi_new")
        )
    else:
        if result["status"] == 1:  # player has no valid move, skip turn
            board.turn = BLACK if board.turn == WHITE else WHITE
            game.board = board.export()
        if board.turn == BLACK:
            turn = bot.get_contact(game.black_player).name
        else:
            turn = bot.get_contact(
                game.p2 if game.black_player == game.p1 else game.p1
            ).name
        text = f"{board.get_disk(board.turn)} {turn} it's your turn...\n\n{board}\n\n{board.get_score()}"
    return text
