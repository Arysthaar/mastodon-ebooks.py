from ananas import PineappleBot, hourly, schedule, reply, daily
ebooks = __import__("mastodon-ebooks")

class ebooksBot(PineappleBot):
  def start(self):
    try:
      self.visibility = str(self.config.visibility)
      if self.visibility not in ['public', 'unlisted', 'private', 'direct']:
        self.visibility = 'unlisted'
    except:
      self.visibility = 'unlisted'
    try:
      self.bot_name = str(self.config.bot_name)
    except:
      self.bot_name = ""
    self.scrape()

  # clear notifications in case the bot will be run from mastodon-ebooks.py
  def close(self):
    self._Mastodon__api_request('POST', '/api/v1/notifications/clear')

  @daily()
  def scrape(self):
    ebooks.scrape(self.mastodon)

  #@hourly(minute=7)
  @hourly(minute=37)
  @daily(hour=13, minute=12)
  @daily(hour=16, minute=20)
  def toot(self):
    msg = ebooks.generate(500)
    self.mastodon.status_post(msg, visibility = self.visibility)

  @reply
  def reply(self, mention, user):
    ebooks.reply(self.mastodon)
