from discord import AudioSource 

class Song:
  url: str
  source: AudioSource
  title: str
  author: str

  def __init__(self, url, title, author, source):
    self.url = url
    self.source = source
    self.title = title
    self.author = author

  def getSource(self):
    return self.source
  
  def getUrl(self):
    return self.url
  
  def getTitle(self):
    return self.title
  
  def getAuthor(self):
    return self.author