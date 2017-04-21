import csv
import string
import sys
import time
import random


# Function used to read a db file. encoding changed to utf-8-sig
# to avoid printing BOM (byte order mark)
# Returns a list of records. Every record is a touple of two other touples.
def read():
    music = []
    with open('music.csv', 'r', encoding='utf-8-sig') as db:
        reader = csv.reader(db, delimiter='|', quotechar='"')
        for artist, album, year, genre, length in reader:
            name = (artist.strip(), album.strip())
            information = (year.strip(), genre.strip(), length.strip())
            music.append((name, information))
    return music


# Function used to write record into db.
def write(record):
    name = record[0]
    information = record[1]
    row = [name[0], name[1], information[0], information[1], information[2]]
    with open('music.csv', 'a') as db:
        writer = csv.writer(db, delimiter='|')
        writer.writerow(row)


# function used to find a record in db. Key is defining by what
# we are searching. Returns all matching records in original form:
# (list of touples, every touple contain two other touples)
def find(key):
    keys = {2: "artist's name", 3: "year of release", 4: "album's name",
            5: "genre", 6: "fragment of album name",
            8: "genre", 9: "artist's name"}
    music = read()
    result = []
    try:
        value = input("Enter " + keys[key] + ": ")
        if key == 2 or key == 9:
            for record in music:
                if record[0][0].lower() == value.lower():
                    result.append(record)
        elif key == 3:
            for record in music:
                if record[1][0].lower() == value.lower():
                    result.append(record)
        elif key == 4:
            for record in music:
                if record[0][1].lower() == value.lower():
                    result.append(record)
        elif key == 5 or key == 8:
            for record in music:
                if record[1][1].lower() == value.lower():
                    result.append(record)
        elif key == 6:
            for record in music:
                if value.lower() in record[0][1].lower():
                    result.append(record)
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nYou have exited a collector")
    if result == []:
        print("\nNo matching albums")
    return result


# checking if record with given name is already in collection
# returns True / False
def is_already_in_collection(name):
    try:
        with open('music.csv', 'r', encoding='utf-8-sig') as db:
            reader = csv.reader(db, delimiter='|', quotechar='"')
            for artist, album, year, genre, length in reader:
                if name == (artist.strip(), album.strip()):
                    result = True
                    break
                else:
                    result = False
    except FileNotFoundError:
        # quite obvious that when there is no file, there is nothing in it :)
        result = False
    return result


# joins record (multitupeled tuple of list or tuples -
# whatever, until it's only 3 levels deep) to a string,
# and formats it to nicer looking one for printing
def join_record(record):
    row = []
    for item in record:
        if isinstance(item, (list, tuple)):
            for i in item:
                if isinstance(i, (list, tuple)):
                    for x in i:
                        row.append(x)
                else:
                    row.append(i)
        else:
            row.append(item)
    return (' - '.join(row))


# function which forces user to format correct time input,
# and helps formating it
def time_input_guide():
    loop = True
    while loop is True:
        try:
            time = input("time: ")
            if ":" in time:
                time = time.split(':')
                for i in time:
                    if int(i) in range(0, 59):
                        loop = False
                    else:
                        print("Wrong time format! Enter as MM:SS or HH:MM:SS")
                        loop = True
                        break
            else:
                print("Wrong time format! Enter as MM:SS or HH:MM:SS")
                loop = True
        except ValueError:
            print("Wrong time format! Enter as MM:SS or HH:MM:SS")
            loop = True
        except (KeyboardInterrupt, EOFError):
            sys.exit("\nYou have exited a collector")
    if len(time[-1]) == 1:  # count backward to handle both HH:MM:SS and MM:SS
        time[-1] = '0' + time[-1]
    if len(time) == 3:
        if int(time[-3]) == 0:
            del time[-3]  # deleting HH when 0
        else:
            if len(time[-2]) == 1:  # formating M to MM only when H egsist
                time[-2] = '0' + time[-2]
    return ':'.join(time)


menu = '''\nWelcome in the CoolMusic! Choose the action:

   1) Add new album
   2) Find albums by artist
   3) Find albums by year
   4) Find musician by album
   5) Find albums by letter(s)
   6) Find albums by genre
   7) Calculate the age of all albums
   8) Choose a random album by genre
   9) Show the amount of albums by an artist
  10) Find the longest-time album
   0) Exit'''

print(menu)  # before loop. only once, utntil not called again

while True:  # program main loop.

    try:
        action = input("\nChoose action ('M' to show menu): ")

        if action == "1":  # adding new definition
            new_artist = input("Enter Artist name: ")
            new_album = input("Enter Album name: ")
            new_name = (new_artist, new_album)
            music = read()
            if is_already_in_collection(new_name):
                print("\nAlbum already in collection!")
            else:
                new_year = input("Enter year of release: ")
                new_genre = input("Enter genre: ")
                new_length = time_input_guide()
                new_information = (new_year, new_genre, new_length)
                write((new_name, new_information))
                print("\nSuccessfully added!")
            print(join_record((new_name, new_information)))  # printing added

        #  all searching options works on one alghoritm. see funtion comment
        elif action in ["2", "3", "4", "5", "6"]:  #
            for record in find(int(action)):
                print(join_record(record))

        elif action == "7":  # printing all albums with added age of album
            music = read()
            actual_year = int(time.strftime("%Y"))
            for record in music:
                try:
                    print(join_record(record[0]), "-",
                          actual_year - int(record[1][0]), "yo")
                except ValueError:
                    print(join_record(record[0]), "- Wrong year of release")

        # random album by genre. Uses find(),
        # than chose random from result list
        elif action == "8":
            result = find(int(action))
            try:
                print(join_record(random.choice(result)))
            except(ValueError, IndexError):
                pass

        # number of albums by artist. Uses find(),
        # than print a len of result list
        elif action == "9":
            result = find(int(action))
            if len(result) > 0:
                print(len(result), "album(s)")

        # finds a longest album.
        # first make a tuple (orginal record, length of album in sec.)
        # than sort by length, and returns orginal record of sorted tuple
        elif action == "10":
            music = read()
            music_sort = []
            for record in music:
                music_sort.append(
                      (record, sum(int(x) * 60 ** i for i, x in
                       enumerate(reversed(record[1][2].split(':'))))))
            music_sort = sorted(music_sort, key=lambda x: x[1])
            print(join_record(music_sort[-1][0]))

        elif action.lower() == "m":  # printing menu
            print(menu)

        elif action == "0":  # goodbye
            sys.exit("\nYou have exited a collector")

        else:  # for entering command out of menu
            print("\nWrong choose!\nTry again")

    # KI and EOFE causes program quiting, FNFE allows to create a new file
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nYou have exited a collector")
    except FileNotFoundError:
        print("\nMissing database file. Add new album to make new one,")
        print("or check the program folder")
    # VE is raised when DB has empty lines. Need to be changed in future
    except ValueError:
        sys.exit("\nProblem occured while loading database: Invalid Database")
