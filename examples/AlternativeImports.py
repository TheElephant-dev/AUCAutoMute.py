
# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.simple',
                      'cogs.members',
                      'cogs.owner']


# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

