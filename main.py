import finder
import scraper
import reader

with open('log.txt', 'w', newline = '', encoding = 'UTF-8') as writer:
    writer.write("Master: START--START--START--START--START\n")
    print("Master: START--START--START--START--START")
"""
    * Starting point, give it a real player ID
    * zsda123 is only a placeholder!!!
    * If it happens to be a real ID or your ID, I apologize for that!
"""
    finder.main(writer, "zsda123")

    with open('userIdList.txt', 'r', newline = '', encoding = 'UTF-8') as f:
        userIdListStr = f.read()

    userIdList = userIdListStr.split()

    scraper.main(writer, userIdList)

    reader.main(writer)

    writer.write("Master: DONE--DONE--DONE--DONE--DONE\n")
    print("Master: DONE--DONE--DONE--DONE--DONE")
