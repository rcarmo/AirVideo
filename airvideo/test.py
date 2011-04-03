from client import AVClient

c = AVClient("10.0.0.3")
lom = c.browse("1fd9e1cf-ef8d-4605-a061-553346d12b9b")
lom_s1 = lom[0]
print lom_s1.contents()[3].live_url()