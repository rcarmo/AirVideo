from client import AVClient

c = AVClient("10.0.0.10")
all_dirs = c.browse()
print all_dirs[0].contents()[2].contents()[1].contents()[2].contents()[11].live_url()