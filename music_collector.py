import csv
import string
import sys
import time
import random
import itertools


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


# funct. used to find a record in db. Key is defining what we are looking for,
# value is what we expect to find.
# returns all records in original form
# (list of touples, every touple contain two other touples)
def find(key, value):
    music = read()
    result = []
    if key == 'artist':
        for record in music:
            if record[0][0].lower() == value.lower():
                result.append(record)
    elif key == 'year':
        for record in music:
            if record[1][0].lower() == value.lower():
                result.append(record)
    elif key == 'album':
        for record in music:
            if record[0][1].lower() == value.lower():
                result.append(record)
    elif key == 'genre':
        for record in music:
            if record[1][1].lower() == value.lower():
                result.append(record)
    elif key == 'letter':
        for record in music:
            if value.lower() in record[0][1].lower():
                result.append(record)
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
# whatever until it's only 3 levels deep) to a string,
# and formats it to nicer looking one when printed
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
    if len(time[-1]) == 1:
        time[-1] = '0' + time[-1]
    if len(time) == 3:
        if int(time[-3]) == 0:  # counting list from behind to handle both HH:MM:SS and MM:SS
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

        elif action == "2":  # searching by appellation
            expected = input("\nEnter Artist name: ")
            result = find('artist', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                for record in result:
                    print(join_record(record))

        # show all avaible appelations in alphabetical order
        elif action == "3":
            expected = input("\nEnter year of release: ")
            result = find('year', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                for record in result:
                    print(join_record(record))

        elif action == "4":  # searching appelation by first letter
            expected = input("\nEnter album name: ")
            result = find('album', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                found_artists = []
                for record in result:
                    if record[0][0] not in found_artists:
                        found_artists.append(record[0][0])
                for item in found_artists:
                    print(item)

        elif action == "5":
            expected = input("\nEnter fragment of album name: ")
            result = find('letter', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                for record in result:
                    print(join_record(record))

        elif action == "6":
            expected = input("\nEnter genre: ")
            result = find('genre', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                for record in result:
                    print(join_record(record))

        elif action == "7":
            music = read()
            actual_year = int(time.strftime("%Y"))
            for record in music:
                try:
                    print(join_record(record[0]), "-", actual_year - int(record[1][0]), "yo")
                except ValueError:
                    print(join_record(record[0]), "- Wrong year of release")

        elif action == "8":
            expected = input("\nEnter a genre: ")
            result = find('genre', expected)
            if result == []:
                print("\nNo matching albums")
            else:
                print(join_record(random.choice(result)))

        elif action == "9":
            expected = input("\nEnter Artist name: ")
            result = find('artist', expected)
            print(expected, ":", len(result), "album(s)")

        elif action.lower() == "m":  # printing menu
            print(menu)

        elif action == "10":
            music = read()
            music_sort = []
            for record in music:
                music_sort.append((record, sum(int(x) * 60 ** i for i, x in enumerate(reversed(record[1][2].split(':'))))))
            music_sort = sorted(music_sort, key=lambda x: x[1])
            print(join_record(music_sort[-1][0]))

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
