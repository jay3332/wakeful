import discord
from discord.ext import menus

class Paginator(menus.ListPageSource):
    async def format_page(self, menu, embed : discord.Embed):
        em = embed.to_dict()
        if em.get("footer") is not None:
            if em.get("footer").get("text") is not None:
                if not "Page: " in em.get("footer").get("text"):
                    em["footer"]["text"] = "".join(f"{em['footer']['text']} • Page: {menu.current_page+1}/{menu.source.get_max_pages()}" if em['footer']["text"] is not None else f"Page: {menu.current_page+1}/{menu.source.get_max_pages()}")
                else:
                    em["footer"]["text"].replace(f"Page: {menu.current_page}/{menu.source.get_max_pages()}", f"Page: {menu.current_page+1}/{menu.source.get_max_pages()}")
        else:
            em["footer"] = {}
            em["footer"]["text"] = f"Page: {menu.current_page}/{menu.source.get_max_pages()}"
        em = discord.Embed().from_dict(em)
        return em