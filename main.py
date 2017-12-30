import finder
import scraper
import reader

with open('log.txt', 'w', newline = '', encoding = 'UTF-8') as writer:
    writer.write("Master: START--START--START--START--START\n")
    print("Master: START--START--START--START--START")
    finder.main(writer, "YechenDetoxic")

    with open('userIdList.txt', 'r', newline = '', encoding = 'UTF-8') as f:
        userIdListStr = f.read()

    userIdList = userIdListStr.split()

    scraper.main(writer, userIdList)

    reader.main(writer)

    writer.write("Master: DONE--DONE--DONE--DONE--DONE\n")
    print("Master: DONE--DONE--DONE--DONE--DONE")
