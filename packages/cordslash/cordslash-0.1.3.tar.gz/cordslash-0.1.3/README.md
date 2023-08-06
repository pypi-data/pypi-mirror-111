# Cordslash
cordslash is a *WIP* discord slash commands wrapper, that is built on the [corded](https://github.com/vcokltfre/Corded) framework by vcokltfre.
Expect more changes/features to be added in the future, currently undocumented but will be soon
*PR's are welcome*

**MAKE SURE TO INSTALL CORDED OTHERWISE USE THE POETRY ENV**

# example.py

```py
import corded
import cordslash

intents = corded.Intents.default()
intents.guild_members = True

bot = cordClient(token="BOT_TOKEN", app_id=BOT_ID, intents=intents)

@bot.command(name="wave", guild_ids=[12345678910], description="Say hello to a user")
async def wave(ctx: cordslash.Context, user: cordslash.User) -> None:
    await ctx.send(f":wave: <@{user}>!")

bot.start()
```
