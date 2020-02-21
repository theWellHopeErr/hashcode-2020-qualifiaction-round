import sys
import os

# Parsing input
fileName = sys.argv[1]
f = open(f'{fileName}.txt')

scoreFile = open("scores.txt", "r+")
score = int(scoreFile.readline())
scoreFile.seek(0, os.SEEK_SET) 

nBooks, nLibraries, nDays = map(int, f.readline().split())
bookScores = list(map(int, f.readline().split()))
libraries = []
isBookShipped = [False] * nBooks

for i in range(nLibraries):
    nBooksinL, nSignup, shippingPerDay = map(int, f.readline().split())
    bookList = list(map(int, f.readline().split()))
    bookList.sort(key=lambda book: bookScores[book], reverse=True)
    sumOfBookScores = sum([bookScores[book] for book in bookList])
    avgOfBookScores = sumOfBookScores/nBooksinL
    booksOverAverageScore = [book for book in bookList if bookScores[book] >= avgOfBookScores]
    libraries.append(
        {
            "id": i,
            "nBooks": nBooksinL,
            "signupDays": nSignup,
            "shippingPerDay": shippingPerDay,
            "bookList": bookList,
            'sumOfBookScores': sumOfBookScores,
            'booksOverAverageScore': booksOverAverageScore
        }
    )

libraries.sort(key=lambda x: x['signupDays'] + 1/x['sumOfBookScores'] +
               (1/x['nBooks'])+(0.0025/x['shippingPerDay'])+(0.00025/len(x['booksOverAverageScore'])))

# libraries.sort(key=lambda x: 0.9*x['signupDays'] + 1/x['sumOfBookScores'] + 0.0001*x['nBooks']/x['shippingPerDay'])

# output variables
signedUpLibraries = []
booksScannedFromLibraries = dict()
remainingDays = nDays

for i, library in enumerate(libraries):
    if remainingDays < library['signupDays']:
        break
    signedUpLibraries.append(library['id'])
    remainingDays -= library['signupDays']
    booksScannedFromLibraries[library['id']] = []
    for book in library['bookList'][:remainingDays * library['shippingPerDay']]:
        if not isBookShipped[book]:
            booksScannedFromLibraries[library['id']].append(book)
            isBookShipped[book] = True
    if len(booksScannedFromLibraries[library['id']]) == 0:
        signedUpLibraries.pop()
        remainingDays += library['signupDays']

# print(nBooks, nLibraries, nDays)
# print(bookScores)
# print(libraries)

# write result in x_out.txt file
outFile = open(f"{fileName}_out.txt", "w+")
outFile.write(f"{len(signedUpLibraries)}\n")
# print(len(signedUpLibraries))
for libraryID in signedUpLibraries:
    booksScanned = booksScannedFromLibraries[libraryID]
    outFile.write(f"{libraryID} {len(booksScanned)}\n")
    # print(libraryID, len(booksScanned))
    for i,book in enumerate(booksScanned):
        if i == len(booksScanned)-1:
            outFile.write(f"{book}\n")
        else:
            outFile.write(f"{book} ")
        score += bookScores[book]
    print(*booksScanned)

scoreFile.write(str(score))
f.close()
outFile.close()
scoreFile.close()