def is_owner(bot, user):
    if user.id in bot.owner_ids:
        return True
    else:
        return False