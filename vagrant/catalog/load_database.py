#!/usr/bin/env python

# Running this script will load the default data into the database
# NOTE: Be sure to create the database before running this script

# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Book, User

# Setup and configure the connection to the database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Function for adding Categories to the category table
def addCategory(newCategory, user_id):
    newEntry = Category(name=newCategory, user_id=user_id)
    session.add(newEntry)
    session.commit()


# Function for adding Books to the book table
def addBook(newBook, description, category_id, user_id):
    newEntry = Book(name=newBook, description=description, category_id=category_id, user_id=user_id)
    session.add(newEntry)
    session.commit()


# Function for adding the default admin user
def addUser(userName, email, pic):
    newEntry = User(name=userName, email=email, picture=pic)
    session.add(newEntry)
    session.commit()


# Add the default categories here
addCategory("Science Fiction", 1)
addCategory("Fantasy", 1)
addCategory("History", 1)
addCategory("Philosophy", 1)
addCategory("Scientific Non-Fiction", 1)
addCategory("Reference", 1)


# Add the default books here
addBook("Game of Thrones", "Winter is coming.  Such is the stern motto of House Stark, the northernmost of the fiefdoms that owe allegiance to King Robert Baratheon in for off King's Landing.  There eddard Stark of Winterfell rules in Robert's name.  There his family dwells in peace and comfort: his proud wife, Catelyn; his sons Robb, Brandon, and Rickon; his daughters Sansa and Arya; and his bastard son, Jon Snow.  Far to the north, behind the Wall, lie savage Wildlings and worse - unnatural things relegated to myth during the centuries long summer, but proving all too real and all too deadly in the turning of the season.", 2, 1)
addBook("Starship Troopers", "Starship Troopers is a classic novel by one of science fiction's greatest writers of all time and is now a Tri-Star movie. In one of Heinlein's most controversial bestsellers, a recruit of the future goes through the toughest boot camp in the universe -- and into battle with the Terran Mobile Infantry against mankind's most frightening enemy.", 1, 1)
addBook("The Ape That Understood The Universe", "The Ape that Understood the Universe is the story of the strangest animal in the world: the human animal. It opens with a question: How would an alien scientist view our species? What would it make of our sex differences, our sexual behavior, our child-rearing patterns, our moral codes, our religions, our languages, and science? The book tackles these issues by drawing on ideas from two major schools of thought: evolutionary psychology and cultural evolutionary theory. The guiding assumption is that humans are animals, and that like all animals, we evolved to pass on our genes. At some point, however, we also evolved the capacity for culture - and from that moment, culture began evolving in its own right. This transformed us from a mere ape into an ape capable of reshaping the planet, travelling to other worlds, and understanding the vast universe of which we're but a tiny, fleeting fragment.", 5, 1)
addBook("The Coddling of the American Mind", "The generation now coming of age has been taught three Great Untruths: Their feelings are always right; They should avoid pain and discomfort; and they should look for faults in others and not themselves.  These three Great Untruths are part of a larger philosophy that sees young people as fragile creatures who must be protected and superised by adults.  But despise the good intentions of the adults who impart them, the Great Untruths are harming kids by teaching them the opposite of ancient wisdom and the opposite of modern psychological findings of grit, growth, and antifragility.  The result is rising rates of depression and anxiety, along with enless stories of college campuses torn apart by moralistic divisions and mutual recriminations.", 5, 1)
addBook("Jurassic Park", "An astonishing technique for recovering and cloning dinosaur DNA has been discovered.  Now humankind's most thrilling fantasies have come true.  Creatures exctinct for eons roam Jurassic Park with their awesome presence and profound mystery, and all the world can visit them - for a price.      Until something goes wrong...", 1, 1)
addBook("The Republic", "Presented in the form of a dialogue between Socrates and three different interlocutors, it is an inquiry into the notion of a perfect community and the ideal individual within it.  During the conversation other questions are raise: What is goodness; what is reality; what is knowledge?  The Republic also addresses the purpose of education and the role of both women and men as 'guardians' of the people.  With remarkable lucidity and deft use of alleory, Plato arrives at a depiction of a state bound by harmony and ruled by 'Philosopher Kings'.", 4, 1)
addBook("The Screwtape Letters", "The Screwtape Letters by C.S. Lewis is a classic masterpiece of religious staire that entertains readers with its sly and ironic portrayal of human life and foibles from the vantage point of Screwtape, a highly placed assistant to 'Our Father Below'.  At once wildly comic, deadly serious, and strikingly original, C.S. Lewis's The Screwtape Letters is the most engaging account of temptation - and triumph over it - ever written.", 4, 1)
addBook("The Trainer's Tool Kit", "The Trainer's Tool Kit has long been a vluaed guide for trainers and managers in need of a quick refresher.  Now completely updated with hundreds of ready-to-use techniques, the book is still the perfect resource for new trainers, managers who are suddenly asked to train, and training professionals in need of a quick refresher.", 6, 1)
addBook("Kismet Hacking", "Unlike other wireless networking books that have been published in recent years that geared towards Windows users, Kismet Hacking is geared to those individuals that use the Linux operating system. People who use Linux and want to use wireless tools need to use Kismet. Now with the introduction of Kismet NewCore, they have a book that will answer all their questions about using this great tool. This book continues in the successful vein of books for wireless users such as WarDriving: Drive, Detect Defend", 6, 1)
addBook("How Do You Kill 11 Million People", "In this compact, nonpartisan book, Andrews urges readers to be 'careful students' of the past, seeking accurate, factural accounts of events and decisions that illuminate choices we face now.  By considering how the Nazi German regime was able to carry out over 11 million institutional killings between 1933 and 1945, Andrews advocates for an informed population that demands honesty and integrity from its leaders and from each other.", 3, 1)
addBook("The Gulag Archipelago", "Volume 1 of the gripping epic masterpiece, Solzhenitsyn's chilling report of his arrest and interrogation, which exposed to the world the vast bureaucracy of secret police that haunted Soviet society", 3, 1)

addUser("DefaultAdmin", "default@admin.com", "")

print("Added books to database!")
