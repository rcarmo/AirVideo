from airvideo.client import AVClient
import os


def main():
  # connect
  c = AVClient('localhost', password="password")

  # look for our folder
  path = filter(lambda x: x.name == 'my videos', c.browse()[0].contents)[0].path

  # get data for a subfolder
  print map(lambda x: x.detail, filter(lambda x: not x.isFolder,c.browse(path + "/sample")))

  # get queue info
  print c.get_queue()

if __name__ == '__main__':
  main()
