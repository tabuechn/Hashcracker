import hashlib
import string
import itertools
import threading
import time

password = input("What do you want to crack?\n").encode("utf8")

hashPW = hashlib.sha1(password).hexdigest()
correctPassword = None
possibleCharacters = string.ascii_letters + string.punctuation + string.digits
done = False
ts = time.time()


class CrackerThread(threading.Thread):
    def __init__(self, length):
        threading.Thread.__init__(self)
        self.length = length

    def run(self):
        global password, hashPW, correctPassword, possibleCharacters, done
        for p in itertools.product(possibleCharacters, repeat=self.length):
            if done:
                break
            pwString = ''.join(p).encode("utf8")
            testHash = hashlib.sha1(pwString).hexdigest()
            if testHash == hashPW:
                done = True
                correctPassword = pwString
                break
        newTs = (time.time() - ts) / 60.0
        print("Thread with the length of " +str(self.length) + " is done after " + str(newTs))


print ("The Hash is: " + hashPW)

threads = []

for i in range(1, len(password)+1):
    thread = CrackerThread(i)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


if correctPassword is None:
    print("Password not found")
else:
    print("The Password is: " + correctPassword.decode("utf8"))


